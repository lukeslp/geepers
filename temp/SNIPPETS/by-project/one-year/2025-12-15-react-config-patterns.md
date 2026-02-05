# Code Snippets: React Configuration Patterns
**Project**: one-year
**Date**: 2025-12-15
**Context**: Vite + React configuration for deep path deployment

## Vite Configuration for Nested Deployment

### Pattern: Base Path Configuration
**File**: `vite.config.ts`
**Use Case**: Deploying React app to nested URL path

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [react(), tailwindcss()],

  // Critical: Set base path for nested deployment
  base: '/datavis/one-year/google-trends-react/',

  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
    },
  },

  // Custom root directory
  root: path.resolve(import.meta.dirname, "client"),

  // Custom output directory
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true,
  },

  server: {
    port: 3000,
    strictPort: false,
    host: true,
  },
});
```

**Key Points**:
- `base` must match the URL path where the app will be deployed
- `root` specifies the source directory (client/)
- `outDir` controls where built files go (dist/public/)
- `import.meta.dirname` is the Vite replacement for `__dirname`

## Router Configuration with Base Path

### Pattern: Wouter Router with Base URL
**File**: `App.tsx`
**Use Case**: Client-side routing with nested deployment path

```typescript
import { Route, Switch, Router as WouterRouter } from "wouter";

// Get base path from Vite's BASE_URL environment variable
const basePath = import.meta.env.BASE_URL;

function Router() {
  return (
    <WouterRouter base={basePath}>
      <Switch>
        <Route path={"/"} component={Home} />
        <Route path={"/cinematic"} component={Cinematic} />
        <Route path={"/404"} component={NotFound} />
        <Route component={NotFound} /> {/* Fallback */}
      </Switch>
    </WouterRouter>
  );
}
```

**Key Points**:
- `import.meta.env.BASE_URL` automatically set by Vite from config `base`
- Wouter's `base` prop strips the base path from routes
- Routes defined as `/` will resolve to `/datavis/one-year/app-name/`
- Fallback route catches all unmatched paths

### Alternative: React Router with Basename
**Use Case**: If using React Router instead of Wouter

```typescript
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  const basePath = import.meta.env.BASE_URL;

  return (
    <BrowserRouter basename={basePath}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cinematic" element={<Cinematic />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Data Consolidation Pattern

### Pattern: Merging Multiple JSON Data Sources
**Use Case**: Consolidating overlapping datasets with different schemas

```javascript
// Approach: Load all sources, reconcile dates, merge fields
const sources = [
  { file: 'trends_data.json', dateField: 'week_ending' },
  { file: 'sentiment_viz.json', dateField: 'week_ending' },
  { file: 'sentiment_timeline.json', dateField: 'week_ending' }
];

// Step 1: Parse and normalize dates
const normalized = sources.map(source => {
  const data = JSON.parse(fs.readFileSync(source.file));
  return data.map(item => ({
    ...item,
    date: new Date(item[source.dateField])
  }));
});

// Step 2: Find common date range
const allDates = normalized.flat().map(d => d.date);
const minDate = new Date(Math.min(...allDates));
const maxDate = new Date(Math.max(...allDates));

// Step 3: Merge by date key
const merged = {};
normalized.forEach(dataset => {
  dataset.forEach(item => {
    const key = item.week_ending;
    merged[key] = { ...merged[key], ...item };
  });
});

// Step 4: Export unified structure
const unified = Object.values(merged).sort((a, b) =>
  new Date(a.week_ending) - new Date(b.week_ending)
);

fs.writeFileSync('unified_data.json', JSON.stringify(unified, null, 2));
```

**Result**: Single source of truth with 87 weeks of data (2023-11-05 to 2025-06-29)

## Build and Deployment Commands

### Pattern: Clean Build Process
**Use Case**: Ensuring fresh build with no cache issues

```bash
# Clean previous builds
rm -rf node_modules dist

# Fresh install
pnpm install

# Build for production
pnpm build

# Verify output
ls -la dist/public/
```

### Pattern: Development vs Production Testing
**Use Case**: Comparing dev and prod behavior

```bash
# Development mode (hot reload, source maps)
pnpm dev
# Opens at http://localhost:3000
# Vite serves from client/ directory

# Production build
pnpm build
# Output to dist/public/

# Test production build locally
pnpm preview
# Serves built files from dist/public/
```

## Debugging Blank Screen Issues

### Checklist: React App Shows Blank Screen
1. **Check browser console** - Look for module loading errors
2. **Check network tab** - Verify all assets load (JS, CSS)
3. **Check base path** - Ensure Vite `base` matches deployment URL
4. **Check router base** - Ensure router base matches Vite base
5. **Check index.html** - Verify script tags have correct paths
6. **Test dev mode** - Compare `pnpm dev` vs `pnpm build && pnpm preview`
7. **Check asset paths** - Look for 404s on CSS/JS in network tab

### Pattern: Asset Path Debugging
```javascript
// In browser console
console.log('Base URL:', import.meta.env.BASE_URL);
console.log('Mode:', import.meta.env.MODE);
console.log('Dev:', import.meta.env.DEV);

// Check loaded scripts
Array.from(document.scripts).forEach(s =>
  console.log('Script:', s.src)
);

// Check loaded stylesheets
Array.from(document.styleSheets).forEach(s =>
  console.log('Style:', s.href)
);
```

## Lessons Learned

### Issue: Blank Screen Despite Successful Build
**Symptoms**:
- `pnpm build` completes without errors
- No TypeScript compilation errors
- Files appear in dist/public/
- Browser shows blank white screen
- No obvious console errors

**Potential Causes**:
1. Asset paths incorrect (base path mismatch)
2. Router configuration doesn't match deployment path
3. Entry point (index.html) has wrong script paths
4. Server routing doesn't support SPA (returns 404 for routes)
5. CORS issues with data files
6. JavaScript module loading failures

**Investigation Steps**:
1. Test in dev mode (`pnpm dev`) to see if app works
2. Inspect network tab for failed requests
3. Check console for errors (may be silent in production)
4. Verify built index.html has correct script/CSS paths
5. Test with simplified Vite config (minimal plugins)
6. Check server configuration for SPA support

### Working Alternatives
If React deployment fails, static HTML alternatives work reliably:
- Timeline analysis (timeline_dashboard.html)
- Weekly searches visualization
- Index.html with D3.js visualizations

These avoid build complexity and deploy as simple static files.

## Tags
- vite
- react
- typescript
- deployment
- nested-paths
- spa-routing
- troubleshooting
- data-consolidation
