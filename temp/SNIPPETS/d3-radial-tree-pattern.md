# D3.js Radial Tree Pattern

**Source**: `/home/coolhand/html/datavis/language-tree/js/radial.js`
**Date**: 2025-12-15
**Use Case**: Hierarchical data visualization with radial layout (phylogenetic trees, org charts, language families)

## Core Pattern

```javascript
/**
 * Create a radial tree visualization with D3.js
 * Features: zoom/pan, filtering, interactive hover states, SVG filters
 */
export function createRadialTree(container, data, options = {}) {
    // Configuration
    const margin = 150;
    let width = container.clientWidth || 1200;
    let height = container.clientHeight || 1200;
    let radius = Math.min(width, height) / 2 - margin;

    // SVG setup
    const svg = d3.select(container)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');

    // Main group centered for radial layout
    const g = svg.append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // Create hierarchy and tree layout
    const root = d3.hierarchy(data);
    const tree = d3.tree()
        .size([2 * Math.PI, radius])
        .separation((a, b) => (a.parent === b.parent ? 1 : 2) / a.depth);

    tree(root);

    // Radial link generator
    const linkGenerator = d3.linkRadial()
        .angle(d => d.x)
        .radius(d => d.y);

    // Draw links
    g.selectAll('.link')
        .data(root.links())
        .join('path')
        .attr('class', 'link')
        .attr('d', linkGenerator)
        .attr('fill', 'none')
        .attr('stroke', d => getColor(d))
        .attr('stroke-width', 1.5)
        .attr('stroke-opacity', 0.4);

    // Draw nodes
    const nodes = g.selectAll('.node')
        .data(root.descendants())
        .join('g')
        .attr('class', 'node')
        .attr('transform', d => `
            rotate(${d.x * 180 / Math.PI - 90})
            translate(${d.y}, 0)
        `);

    nodes.append('circle')
        .attr('r', d => d.children ? 4 : 3)
        .attr('fill', d => getColor(d))
        .attr('filter', 'url(#radial-glow)');

    // Add zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([0.3, 4])
        .on('zoom', (event) => {
            g.attr('transform', `translate(${width / 2}, ${height / 2}) ${event.transform}`);
        });

    svg.call(zoom);

    // Double-click to reset zoom
    svg.on('dblclick.zoom', () => {
        svg.transition()
            .duration(750)
            .call(zoom.transform, d3.zoomIdentity);
    });

    return { update, resize };
}
```

## SVG Filters for Glow Effects

```javascript
function createFilters(svg) {
    const defs = svg.append('defs');

    // Standard glow filter
    const glowFilter = defs.append('filter')
        .attr('id', 'radial-glow')
        .attr('x', '-50%')
        .attr('y', '-50%')
        .attr('width', '200%')
        .attr('height', '200%');

    glowFilter.append('feGaussianBlur')
        .attr('stdDeviation', '2.5')
        .attr('result', 'coloredBlur');

    const glowMerge = glowFilter.append('feMerge');
    glowMerge.append('feMergeNode').attr('in', 'coloredBlur');
    glowMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Strong glow for hover states
    const glowStrong = defs.append('filter')
        .attr('id', 'radial-glow-strong')
        .attr('x', '-50%')
        .attr('y', '-50%')
        .attr('width', '200%')
        .attr('height', '200%');

    glowStrong.append('feGaussianBlur')
        .attr('stdDeviation', '4.5')
        .attr('result', 'coloredBlur');

    const glowStrongMerge = glowStrong.append('feMerge');
    glowStrongMerge.append('feMergeNode').attr('in', 'coloredBlur');
    glowStrongMerge.append('feMergeNode').attr('in', 'SourceGraphic');
}
```

## Dynamic Data Filtering

```javascript
function filterData(node, options) {
    const { showExtinct, selectedFamily, searchTerm } = options;

    const filtered = { ...node };

    if (node.children) {
        filtered.children = node.children
            .map(child => filterData(child, options))
            .filter(child => {
                if (!child) return false;

                // Hide extinct languages if toggled off
                if (!showExtinct && child.extinct && !child.children) {
                    return false;
                }

                // Family filter
                if (selectedFamily !== 'all') {
                    if (child.name !== selectedFamily && !child.children) {
                        return false;
                    }
                }

                // Search filter
                if (searchTerm) {
                    const term = searchTerm.toLowerCase();
                    const matchesName = child.name.toLowerCase().includes(term);
                    const hasMatchingDescendant = child.children && child.children.length > 0;
                    return matchesName || hasMatchingDescendant;
                }

                return true;
            });

        // Remove nodes with no children after filtering
        if (filtered.children.length === 0 && node.children.length > 0) {
            delete filtered.children;
        }
    }

    return filtered;
}
```

## Update Pattern for Live Filtering

```javascript
function update(newOptions) {
    currentOptions = { ...currentOptions, ...newOptions };

    // Rebuild tree with filtered data
    const filteredData = filterData(data, currentOptions);
    root = d3.hierarchy(filteredData);
    tree(root);

    // Update links with transition
    const links = g.selectAll('.link')
        .data(root.links(), d => `${d.source.data.name}-${d.target.data.name}`);

    links.exit()
        .transition()
        .duration(300)
        .attr('stroke-opacity', 0)
        .remove();

    links.enter()
        .append('path')
        .attr('class', 'link')
        .attr('fill', 'none')
        .attr('stroke', d => getColor(d))
        .attr('stroke-width', 1.5)
        .attr('stroke-opacity', 0)
        .merge(links)
        .transition()
        .duration(300)
        .attr('d', linkGenerator)
        .attr('stroke-opacity', 0.4);

    // Similar pattern for nodes...
}
```

## Key Features

1. **Radial Layout**: Uses `d3.tree()` with `size([2 * Math.PI, radius])` for circular arrangement
2. **Zoom/Pan**: Integrated zoom behavior with double-click reset
3. **SVG Filters**: Custom glow effects for visual polish
4. **Data Filtering**: Live update pattern with smooth transitions
5. **Accessibility**: ARIA labels, semantic structure
6. **Responsive**: ViewBox scaling, preserveAspectRatio
7. **Interactive**: Hover states, tooltips, clickable nodes

## Common Use Cases

- Language family trees (phylogenetic visualization)
- Organizational hierarchies
- Taxonomy visualization
- File system trees
- Decision trees
- Class inheritance diagrams

## Performance Notes

- Use `selection.join()` for efficient enter/update/exit
- Implement `separation()` function to prevent overlap
- Consider virtual scrolling for >1000 nodes
- Cache computed positions for resize operations

## Related Patterns

- See `d3-sankey-flow-pattern.md` for flow diagrams
- See `glassmorphism-css-pattern.md` for visual styling
- See `es6-lazy-loading-pattern.md` for module loading
