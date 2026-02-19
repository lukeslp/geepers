# WebSocket ConnectionClosed Graceful Exit Pattern

**Problem**: A generic `except Exception` inside a `websockets` recv() loop swallows `ConnectionClosed` exceptions, causing the loop to continue silently and trigger infinite reconnect cycles. This can fill a disk with logs in hours.

**Fix**: Catch `ConnectionClosed` explicitly *before* the generic handler and `break` out of the recv loop so the outer reconnect logic fires correctly.

## Anti-pattern (causes runaway log growth)

```python
async def listen(ws_url):
    while True:  # outer reconnect loop
        try:
            async with websockets.connect(ws_url) as ws:
                while True:  # inner recv loop
                    try:
                        msg = await ws.recv()
                        process(msg)
                    except Exception as e:
                        # WRONG: ConnectionClosed is caught here,
                        # loop continues, reconnect never happens
                        logger.error(f"recv error: {e}")
        except Exception:
            await asyncio.sleep(5)
```

## Fixed pattern

```python
import websockets.exceptions

async def listen(ws_url):
    while True:  # outer reconnect loop
        try:
            async with websockets.connect(ws_url) as ws:
                while True:  # inner recv loop
                    try:
                        msg = await ws.recv()
                        process(msg)
                    except websockets.exceptions.ConnectionClosed:
                        # CORRECT: break exits inner loop, outer loop reconnects
                        break
                    except Exception as e:
                        logger.error(f"recv error: {e}")
        except Exception:
            await asyncio.sleep(5)
```

## Key rule

Always catch `websockets.exceptions.ConnectionClosed` (or its subclasses `ConnectionClosedOK`, `ConnectionClosedError`) **before** `except Exception` in any websockets recv loop. The `break` statement is intentional — it lets the outer `while True` handle reconnection.

## Discovered

- Project: diachronica/bluesky_firehose
- Date: 2026-02-19
- Impact: 90G runaway log file truncated; disk recovered from 96% to 66% usage
