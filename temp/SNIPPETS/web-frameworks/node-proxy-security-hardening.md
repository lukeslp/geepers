# Node.js Proxy Security Hardening — CORS, Body Cap, Error Scrubbing

**Source**: oss-safeguard-ux / proxy-server.js — 2026-03-07
**Stack**: Node.js (http/https, no framework)

## Problem

A lightweight Node.js proxy that forwards requests to an upstream API (e.g.
HuggingFace) has three common security gaps:

1. `Access-Control-Allow-Origin: *` — allows any origin to make cross-site requests.
2. Unbounded body collection — a malicious client can send a giant payload and
   exhaust memory.
3. Reflecting the full upstream error body to the client — leaks internal API
   details (model names, internal paths, quota info).

## Patterns

### 1 — Restrict CORS to an allowlist

```js
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || 'https://example.com').split(',');

// In the request handler:
const origin = req.headers.origin || '';
if (ALLOWED_ORIGINS.includes(origin)) {
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');  // tells caches that response varies by origin
} else {
  // Respond with the first allowed origin (or omit the header entirely)
  res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGINS[0]);
}
res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
```

### 2 — Body size cap in collectBody()

```js
const MAX_BODY = 512 * 1024; // 512 KB

function collectBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let total = 0;
    req.on('data', c => {
      total += c.length;
      if (total > MAX_BODY) {
        req.destroy(); // abort the connection
        reject(new Error('Request body too large'));
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString()));
    req.on('error', reject);
  });
}
```

Wrap the usage site:

```js
let body;
try {
  body = await collectBody(req);
} catch (err) {
  if (err.message === 'Request body too large') {
    res.writeHead(413, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Request too large' }));
    return;
  }
  throw err;
}
```

### 3 — Sanitize upstream errors before returning to the client

```js
// In the upstream error handler:
hfRes.on('end', () => {
  // Log full body server-side only
  console.error(`Upstream API ${hfRes.statusCode}:`, body.slice(0, 500));

  // Return only a generic message to the client
  const statusCode = hfRes.statusCode >= 500 ? 502 : hfRes.statusCode;
  res.writeHead(statusCode, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Service unavailable. Please try again.' }));
});
```

## Complete Hardened collectBody + CORS Skeleton

```js
const http  = require('http');
const https = require('https');

const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || 'https://example.com').split(',');
const MAX_BODY = 512 * 1024;

function setCORSHeaders(req, res) {
  const origin = req.headers.origin || '';
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  } else {
    res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGINS[0]);
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function collectBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let total = 0;
    req.on('data', c => {
      total += c.length;
      if (total > MAX_BODY) { req.destroy(); reject(new Error('Request body too large')); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString()));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  setCORSHeaders(req, res);

  if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }

  let body;
  try {
    body = await collectBody(req);
  } catch (e) {
    res.writeHead(413, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Request too large' }));
    return;
  }

  // ... forward to upstream, sanitize errors on the way back
});
```

## Notes

- `req.destroy()` in the body cap handler terminates the TCP connection; the
  client receives a socket closed error. This is intentional — you don't want
  to drain a 100 MB upload before responding.
- `Vary: Origin` is critical when the CORS header value changes per request.
  Without it, a CDN may cache a response with one origin and serve it to another.
- Keep `MAX_BODY` consistent with Caddy/nginx `client_max_body_size` to avoid
  confusing error sources.
- If the proxy is loopback-only (Caddy terminates public TLS), the CORS risk is
  reduced but still worth fixing — dev servers and direct localhost access remain
  exposed.
