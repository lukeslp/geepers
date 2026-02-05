# D3.js Sankey Flow Diagram Pattern

**Source**: `/home/coolhand/html/datavis/language-tree/js/sankey.js`
**Date**: 2025-12-15
**Use Case**: Flow visualization for hierarchical data (resource flows, migrations, evolution pathways)

## Core Pattern

```javascript
import * as d3 from 'd3';
import { sankey, sankeyLeft } from 'd3-sankey';

/**
 * Create a Sankey flow diagram with time-based positioning
 * Features: date-based x-axis, custom node sorting, gradient links
 */
export function createSankey(container, data, options = {}) {
    // Dimensions
    const margin = { top: 100, right: 200, bottom: 80, left: 100 };
    let width = container.clientWidth || 1600;
    let height = container.clientHeight || 900;
    let innerWidth = width - margin.left - margin.right;
    let innerHeight = height - margin.top - margin.bottom;

    // SVG setup
    const svg = d3.select(container)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // Time scale for x-axis positioning
    const timeScale = d3.scaleLinear()
        .domain([-4500, 2025])  // Proto-Human to present
        .range([0, innerWidth]);

    // Flatten hierarchy into nodes and links
    const { nodes, links } = flattenHierarchy(data);

    // Create Sankey generator
    const sankeyGenerator = d3.sankey()
        .nodeWidth(6)
        .nodePadding(12)
        .extent([[0, 0], [innerWidth, innerHeight]])
        .nodeAlign(sankeyLeft)
        .nodeSort((a, b) => {
            // Sort by family group, then by value (speaker count)
            const familyCompare = (a.family || '').localeCompare(b.family || '');
            if (familyCompare !== 0) return familyCompare;
            return (b.value || 0) - (a.value || 0);
        });

    // Generate layout
    const { nodes: sankeyNodes, links: sankeyLinks } = sankeyGenerator({
        nodes: nodes.map(d => ({ ...d })),
        links: links.map(d => ({ ...d }))
    });

    // Override x-position based on date
    sankeyNodes.forEach(node => {
        const date = Math.max(-4500, Math.min(2025, node.date || -4500));
        node.x0 = timeScale(date);
        node.x1 = node.x0 + 6;
    });

    // Draw time axis
    const xAxis = d3.axisBottom(timeScale)
        .tickValues([-4500, -3000, -1500, 0, 500, 1000, 1500, 2000])
        .tickFormat(d => {
            if (d < 0) return `${Math.abs(d)} BCE`;
            if (d === 0) return '0';
            return `${d} CE`;
        });

    g.append('g')
        .attr('class', 'time-axis')
        .attr('transform', `translate(0, ${innerHeight + 20})`)
        .call(xAxis);

    // Draw links with gradients
    drawLinks(g, sankeyLinks);

    // Draw nodes
    drawNodes(g, sankeyNodes);

    return { update, resize };
}
```

## Flatten Hierarchy for Sankey

```javascript
/**
 * Convert hierarchical data to Sankey nodes and links
 * Each language becomes a node, parent-child relationships become links
 */
function flattenHierarchy(node, family = null, depth = 0) {
    const nodes = [];
    const links = [];

    function traverse(n, parent = null, currentFamily = null, d = 0) {
        // Determine family (top-level group)
        const nodeFamily = currentFamily || n.name;

        // Create node
        const nodeData = {
            id: n.name,
            name: n.name,
            value: n.speakers || 1000,  // Speaker count for node size
            date: n.date || -4500,
            family: nodeFamily,
            extinct: n.extinct || false,
            depth: d,
            description: n.description || '',
            period: n.period || ''
        };

        nodes.push(nodeData);

        // Create link from parent to this node
        if (parent) {
            links.push({
                source: parent.name,
                target: n.name,
                value: n.speakers || 1000
            });
        }

        // Recurse for children
        if (n.children) {
            n.children.forEach(child => {
                traverse(child, n, nodeFamily, d + 1);
            });
        }
    }

    traverse(node, null, family, depth);

    return { nodes, links };
}
```

## Gradient Links for Flow Visualization

```javascript
function drawLinks(g, links) {
    // Create gradients
    const defs = g.select('defs') || g.append('defs');

    links.forEach((link, i) => {
        const gradientId = `link-gradient-${i}`;

        const gradient = defs.append('linearGradient')
            .attr('id', gradientId)
            .attr('gradientUnits', 'userSpaceOnUse')
            .attr('x1', link.source.x1)
            .attr('x2', link.target.x0);

        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', getColor(link.source))
            .attr('stop-opacity', 0.4);

        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', getColor(link.target))
            .attr('stop-opacity', 0.4);

        link.gradientId = gradientId;
    });

    // Draw link paths
    g.selectAll('.link')
        .data(links)
        .join('path')
        .attr('class', 'link')
        .attr('d', d3.sankeyLinkHorizontal())
        .attr('stroke', d => `url(#${d.gradientId})`)
        .attr('stroke-width', d => Math.max(1, d.width))
        .attr('fill', 'none')
        .attr('opacity', 0.6)
        .on('mouseenter', function(event, d) {
            d3.select(this)
                .attr('opacity', 1)
                .attr('stroke-width', d => Math.max(2, d.width + 1));
        })
        .on('mouseleave', function(event, d) {
            d3.select(this)
                .attr('opacity', 0.6)
                .attr('stroke-width', d => Math.max(1, d.width));
        });
}
```

## Node Rendering with Speaker Count

```javascript
function drawNodes(g, nodes) {
    const nodeGroup = g.selectAll('.node')
        .data(nodes)
        .join('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.x0}, ${d.y0})`);

    // Node rectangles
    nodeGroup.append('rect')
        .attr('width', d => d.x1 - d.x0)
        .attr('height', d => d.y1 - d.y0)
        .attr('fill', d => getColor(d))
        .attr('rx', 2)
        .attr('filter', 'url(#node-glow)')
        .on('mouseenter', function(event, d) {
            showTooltip(event, d);
            d3.select(this)
                .attr('filter', 'url(#node-glow-strong)');
        })
        .on('mouseleave', function(event, d) {
            hideTooltip();
            d3.select(this)
                .attr('filter', 'url(#node-glow)');
        });

    // Node labels
    nodeGroup.append('text')
        .attr('x', d => (d.x1 - d.x0) / 2)
        .attr('y', d => (d.y1 - d.y0) / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'middle')
        .attr('font-size', 10)
        .attr('fill', 'var(--text-primary)')
        .text(d => {
            // Only show label if node is tall enough
            const height = d.y1 - d.y0;
            if (height < 15) return '';
            return d.name;
        });
}
```

## Custom Time Axis with BCE/CE Formatting

```javascript
function drawTimeAxis(g, timeScale, innerHeight) {
    const xAxis = d3.axisBottom(timeScale)
        .tickValues([-4500, -3000, -1500, 0, 500, 1000, 1500, 2000])
        .tickFormat(d => {
            if (d < 0) return `${Math.abs(d)} BCE`;
            if (d === 0) return '0';
            return `${d} CE`;
        })
        .tickSize(6)
        .tickPadding(8);

    g.append('g')
        .attr('class', 'time-axis')
        .attr('transform', `translate(0, ${innerHeight + 20})`)
        .call(xAxis)
        .selectAll('text')
        .attr('fill', 'var(--text-muted)')
        .attr('font-family', 'var(--font-mono)')
        .attr('font-size', 12);

    // Add axis label
    g.append('text')
        .attr('x', timeScale.range()[1] / 2)
        .attr('y', innerHeight + 55)
        .attr('text-anchor', 'middle')
        .attr('fill', 'var(--text-secondary)')
        .attr('font-family', 'var(--font-display)')
        .attr('font-size', 14)
        .text('Timeline of Language Evolution');
}
```

## Update Pattern for Live Filtering

```javascript
function update(newOptions) {
    // Filter data
    const filteredData = filterData(data, newOptions);

    // Regenerate nodes and links
    const { nodes, links } = flattenHierarchy(filteredData);

    // Rebuild Sankey
    const { nodes: sankeyNodes, links: sankeyLinks } = sankeyGenerator({
        nodes: nodes.map(d => ({ ...d })),
        links: links.map(d => ({ ...d }))
    });

    // Update with transitions
    const linkSelection = g.selectAll('.link')
        .data(sankeyLinks, d => `${d.source.id}-${d.target.id}`);

    linkSelection.exit()
        .transition()
        .duration(300)
        .attr('opacity', 0)
        .remove();

    linkSelection.enter()
        .append('path')
        .attr('class', 'link')
        .merge(linkSelection)
        .transition()
        .duration(300)
        .attr('d', d3.sankeyLinkHorizontal())
        .attr('opacity', 0.6);

    // Similar pattern for nodes...
}
```

## Key Features

1. **Time-Based Layout**: Override Sankey x-position with time scale
2. **Gradient Links**: Color transitions along flow paths
3. **Custom Sorting**: Sort nodes by family and speaker count
4. **Interactive Tooltips**: Show details on hover
5. **Dynamic Filtering**: Live updates with smooth transitions
6. **Historical Timeline**: BCE/CE axis formatting

## Common Use Cases

- Language evolution over time
- Population migrations
- Resource flows (energy, money, materials)
- Skill progression paths
- Product journey maps
- Budget allocations

## Performance Notes

- Limit to <500 nodes for smooth interactions
- Use `nodeSort()` to prevent crossing links
- Cache gradient definitions for reuse
- Consider clustering small nodes (<1% of total)

## Related Patterns

- See `d3-radial-tree-pattern.md` for hierarchical trees
- See `d3-timeline-pattern.md` for chronological layouts
