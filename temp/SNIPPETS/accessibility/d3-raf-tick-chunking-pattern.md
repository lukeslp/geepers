# D3 Force Simulation — rAF Tick Chunking

**Category**: accessibility / performance
**Source**: html/datavis/dowjones/script.js (2026-03-08)
**Tags**: d3, force-simulation, requestAnimationFrame, performance, main-thread

## Problem

`d3.forceSimulation` runs synchronously by default, blocking the main thread for several seconds on page load when a graph has many nodes or complex forces. This causes a visible freeze before any interaction is possible.

## Pattern

Stop automatic ticking, then drive the simulation manually in yielding rAF chunks so the browser stays responsive.

```javascript
// Stop automatic ticking — we drive the simulation manually via rAF to avoid
// blocking the main thread for several seconds on page load.
simulation.stop();

let rafId = null;

function tickSimulation() {
    const ticksPerFrame = 3; // tune: fewer = smoother UI, more = faster convergence
    for (let i = 0; i < ticksPerFrame; i++) {
        simulation.tick();
    }
    updatePositions(); // apply new x/y to DOM elements

    if (simulation.alpha() > simulation.alphaMin()) {
        rafId = requestAnimationFrame(tickSimulation);
    } else {
        rafId = null;
    }
}
rafId = requestAnimationFrame(tickSimulation);

// Re-start the rAF loop when user drags a node (simulation may have cooled).
function dragStarted(event, d) {
    if (!event.active && !rafId) {
        rafId = requestAnimationFrame(tickSimulation);
    }
    simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}
```

## Why `ticksPerFrame = 3`?

- `1` tick/frame: smoothest UI but simulation takes ~300 frames (~5s at 60fps) to converge
- `3` ticks/frame: good balance — converges in ~100 frames (~1.7s at 60fps), barely perceptible jank
- `10+` ticks/frame: faster convergence but you start to see jank on slower devices

## Notes

- `updatePositions()` should update SVG `cx`/`cy` attributes (nodes) and `x1/y1/x2/y2` (links) from the simulation data
- This pattern is compatible with D3 v6, v7
- The `rafId` guard prevents double-starting when dragging starts while the simulation is still running
