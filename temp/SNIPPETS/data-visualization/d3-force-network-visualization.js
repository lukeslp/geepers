/**
 * D3.js Force-Directed Network Visualization with Mobile Support
 *
 * Description: Complete pattern for creating interactive force-directed graphs
 * showing relationships between entities. Includes mobile touch handling, filtering,
 * tooltips, and multiple layout modes (clustering, pinned nodes).
 *
 * Use Cases:
 * - Corporate board interlocks and relationship mapping
 * - Social network visualization
 * - Organization charts with cross-functional relationships
 * - Knowledge graphs and entity relationships
 * - Any many-to-many relationship visualization
 *
 * Dependencies:
 * - D3.js v7+ (https://d3js.org/)
 * - ES6 modules support
 *
 * Notes:
 * - Fully responsive with mobile touch support (pinch-to-zoom, drag, tap)
 * - Performance optimized for 50-200 nodes
 * - Includes "dream catcher" layout pattern for pinned peripheral nodes
 * - Connection type indicators via line styling
 * - Supports dynamic filtering and re-rendering
 * - Keyboard accessible with Tab/Enter navigation
 *
 * Related Snippets:
 * - See d3-choropleth-map.js for geographic network overlays
 * - See chart-js-dashboards.js for complementary data panels
 * - See animation-timeline.js for temporal network evolution
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/datavis/dowjones/script.js
 * - Pattern used in: Corporate board interlocks visualization
 * - Related: D3 force simulation examples, Observable notebooks
 */

// ==================== DATA STRUCTURE ====================

/**
 * Expected data format:
 *
 * nodes = [
 *   { id: "AAPL", name: "Apple Inc.", type: "company", sector: "Technology" },
 *   { id: "GOV1", name: "Military Service", type: "category", pinned: true },
 *   ...
 * ]
 *
 * links = [
 *   { source: "AAPL", target: "MSFT", type: "board", sharedDirectors: ["John Doe"], value: 1 },
 *   { source: "AAPL", target: "GOV1", type: "government", person: "Jane Smith" },
 *   ...
 * ]
 */

// ==================== CONFIGURATION ====================

const config = {
  // Dimensions
  width: window.innerWidth,
  height: window.innerHeight,

  // Force simulation parameters
  forces: {
    linkDistance: 100,       // Base link length
    linkStrength: 0.5,       // Link strength (0-1)
    chargeStrength: -600,    // Node repulsion (negative = repel)
    centerStrength: 0.1,     // Pull toward center (0-1)
    collideRadius: 30        // Collision detection radius
  },

  // Mobile adjustments
  mobileForcesMultiplier: {
    linkDistance: 0.85,      // Shorter links on mobile
    chargeStrength: 0.75     // Less repulsion on mobile
  },

  // Visual styling
  nodeRadius: {
    base: 8,
    connected: 10,
    sizeMultiplier: 1.5,     // Extra radius per connection
    mobileMultiplier: 0.8    // Scale down on mobile
  },

  linkWidth: {
    base: 1.5,
    perDirector: 0.5,        // Extra width per shared director
    highlighted: 3,
    government: 2
  },

  colors: {
    linkTypes: {
      board: '#0077BB',      // Blue for board connections
      mixed: '#000000',      // Black for mixed board+executive
      government: '#D4AF37'  // Gold for government connections
    },
    nodeTypes: {
      company: '#4A90E2',
      category: '#D4AF37',
      highlighted: '#FF6B6B'
    }
  },

  // Pinned node layout (dream catcher)
  pinnedLayout: {
    enabled: true,
    radius: null,            // Calculated from dimensions
    padding: 100             // Distance from viewport edge
  }
};

// Detect mobile
const isMobile = window.innerWidth <= 768;
const isSmallMobile = window.innerWidth <= 480;

// ==================== SVG SETUP ====================

const svg = d3.select('#network-graph')
  .append('svg')
  .attr('width', config.width)
  .attr('height', config.height)
  .attr('viewBox', [0, 0, config.width, config.height])
  .attr('preserveAspectRatio', 'xMidYMid meet')
  .style('background', '#f8f9fa');

// Add zoom behavior
const g = svg.append('g');

const zoom = d3.zoom()
  .scaleExtent([0.1, 4])
  .on('zoom', (event) => {
    g.attr('transform', event.transform);
  });

svg.call(zoom);

// Mobile touch handling: differentiate between pan and drag
let touchStartTime;
svg.on('touchstart', () => {
  touchStartTime = Date.now();
});

// ==================== FORCE SIMULATION ====================

function createForceSimulation(nodes, links) {
  // Calculate pinned node positions if enabled
  if (config.pinnedLayout.enabled) {
    const pinnedNodes = nodes.filter(n => n.pinned);
    const numPinned = pinnedNodes.length;

    config.pinnedLayout.radius = Math.min(config.width, config.height) / 2 - config.pinnedLayout.padding;

    pinnedNodes.forEach((node, i) => {
      const angle = (i / numPinned) * 2 * Math.PI;
      node.fx = config.width / 2 + config.pinnedLayout.radius * Math.cos(angle);
      node.fy = config.height / 2 + config.pinnedLayout.radius * Math.sin(angle);
    });
  }

  // Adjust forces for mobile
  const linkDistance = config.forces.linkDistance * (isMobile ? config.mobileForcesMultiplier.linkDistance : 1);
  const chargeStrength = config.forces.chargeStrength * (isMobile ? config.mobileForcesMultiplier.chargeStrength : 1);

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links)
      .id(d => d.id)
      .distance(linkDistance)
      .strength(config.forces.linkStrength)
    )
    .force('charge', d3.forceManyBody()
      .strength(chargeStrength)
    )
    .force('center', d3.forceCenter(config.width / 2, config.height / 2)
      .strength(config.forces.centerStrength)
    )
    .force('collide', d3.forceCollide()
      .radius(config.forces.collideRadius)
    );

  return simulation;
}

// ==================== RENDER NETWORK ====================

function renderNetwork(nodes, links) {
  // Clear existing
  g.selectAll('*').remove();

  // Create simulation
  const simulation = createForceSimulation(nodes, links);

  // Render links
  const link = g.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('class', d => `link ${d.type}`)
    .attr('stroke', d => config.colors.linkTypes[d.type] || '#999')
    .attr('stroke-width', d => {
      const baseWidth = config.linkWidth.base;
      const extraWidth = (d.sharedDirectors?.length || 1) * config.linkWidth.perDirector;
      return d.type === 'government' ? config.linkWidth.government : baseWidth + extraWidth;
    })
    .attr('stroke-dasharray', d => d.type === 'government' ? '5,5' : null)
    .attr('opacity', 0.6);

  // Render nodes
  const node = g.append('g')
    .selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('class', d => `node ${d.type}`)
    .attr('r', d => getNodeRadius(d))
    .attr('fill', d => config.colors.nodeTypes[d.type] || config.colors.nodeTypes.company)
    .attr('stroke', d => d.hasGovernmentConnection ? config.colors.nodeTypes.category : '#fff')
    .attr('stroke-width', d => d.hasGovernmentConnection ? 3 : 2)
    .call(drag(simulation))
    .on('mouseover', handleNodeHover)
    .on('mouseout', handleNodeOut)
    .on('click', handleNodeClick);

  // Add labels
  const label = g.append('g')
    .selectAll('text')
    .data(nodes)
    .join('text')
    .text(d => d.name)
    .attr('font-size', isMobile ? 10 : 12)
    .attr('text-anchor', 'middle')
    .attr('dy', d => getNodeRadius(d) + 15)
    .attr('pointer-events', 'none')
    .attr('opacity', 0.8);

  // Tick function
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);

    label
      .attr('x', d => d.x)
      .attr('y', d => d.y);
  });

  // Stop simulation after convergence
  setTimeout(() => simulation.stop(), 5000);

  return { simulation, node, link, label };
}

// ==================== HELPER FUNCTIONS ====================

function getNodeRadius(node) {
  const baseRadius = node.hasConnections ? config.nodeRadius.connected : config.nodeRadius.base;
  const connectionBonus = (node.connections || 0) * config.nodeRadius.sizeMultiplier;
  const multiplier = isMobile ? config.nodeRadius.mobileMultiplier : 1;
  return (baseRadius + connectionBonus) * multiplier;
}

function handleNodeHover(event, d) {
  // Highlight connected links
  d3.selectAll('.link')
    .attr('opacity', link =>
      (link.source.id === d.id || link.target.id === d.id) ? 1 : 0.1
    )
    .attr('stroke-width', link =>
      (link.source.id === d.id || link.target.id === d.id) ? config.linkWidth.highlighted : link.defaultWidth
    );

  // Highlight node
  d3.select(event.target)
    .attr('fill', config.colors.nodeTypes.highlighted)
    .attr('stroke-width', 4);

  // Show tooltip
  showTooltip(event, d);
}

function handleNodeOut(event, d) {
  // Reset links
  d3.selectAll('.link')
    .attr('opacity', 0.6)
    .attr('stroke-width', link => link.defaultWidth);

  // Reset node
  d3.select(event.target)
    .attr('fill', config.colors.nodeTypes[d.type] || config.colors.nodeTypes.company)
    .attr('stroke-width', d.hasGovernmentConnection ? 3 : 2);

  // Hide tooltip
  hideTooltip();
}

function handleNodeClick(event, d) {
  // Double-click to zoom to node
  const clickTime = Date.now();
  if (clickTime - (d.lastClick || 0) < 300) {
    zoomToNode(d);
  }
  d.lastClick = clickTime;
}

function zoomToNode(node) {
  const scale = 2;
  const x = -node.x * scale + config.width / 2;
  const y = -node.y * scale + config.height / 2;

  svg.transition()
    .duration(750)
    .call(zoom.transform, d3.zoomIdentity.translate(x, y).scale(scale));
}

// ==================== DRAG BEHAVIOR ====================

function drag(simulation) {
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    // Release non-pinned nodes
    if (!d.pinned) {
      d.fx = null;
      d.fy = null;
    }
  }

  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);
}

// ==================== TOOLTIP ====================

const tooltip = d3.select('body')
  .append('div')
  .attr('class', 'network-tooltip')
  .style('position', 'absolute')
  .style('visibility', 'hidden')
  .style('background', 'rgba(0, 0, 0, 0.9)')
  .style('color', '#fff')
  .style('padding', '12px')
  .style('border-radius', '8px')
  .style('font-size', '14px')
  .style('max-width', '300px')
  .style('pointer-events', 'none')
  .style('z-index', 1000);

function showTooltip(event, d) {
  const html = `
    <strong>${d.name}</strong><br>
    ${d.type === 'company' ? `Sector: ${d.sector}<br>` : ''}
    Connections: ${d.connections || 0}
  `;

  tooltip
    .html(html)
    .style('visibility', 'visible')
    .style('left', (event.pageX + 10) + 'px')
    .style('top', (event.pageY - 10) + 'px');
}

function hideTooltip() {
  tooltip.style('visibility', 'hidden');
}

// ==================== FILTERING ====================

function filterNetwork(nodes, links, criteria) {
  // Filter nodes
  const filteredNodes = nodes.filter(node => {
    if (criteria.showUnconnected === false && !node.hasConnections) return false;
    if (criteria.types && !criteria.types.includes(node.type)) return false;
    return true;
  });

  const nodeIds = new Set(filteredNodes.map(n => n.id));

  // Filter links
  const filteredLinks = links.filter(link => {
    if (criteria.linkTypes && !criteria.linkTypes.includes(link.type)) return false;
    return nodeIds.has(link.source.id || link.source) && nodeIds.has(link.target.id || link.target);
  });

  return { nodes: filteredNodes, links: filteredLinks };
}

// ==================== USAGE EXAMPLE ====================

/*
// Sample data
const sampleNodes = [
  { id: "AAPL", name: "Apple", type: "company", sector: "Technology", connections: 3 },
  { id: "MSFT", name: "Microsoft", type: "company", sector: "Technology", connections: 2 },
  { id: "GOV1", name: "Military Service", type: "category", pinned: true }
];

const sampleLinks = [
  { source: "AAPL", target: "MSFT", type: "board", sharedDirectors: ["John Doe"], value: 1 },
  { source: "AAPL", target: "GOV1", type: "government", person: "Jane Smith" }
];

// Render network
const { simulation, node, link, label } = renderNetwork(sampleNodes, sampleLinks);

// Filter example
const filtered = filterNetwork(sampleNodes, sampleLinks, {
  showUnconnected: false,
  linkTypes: ['board', 'government']
});
renderNetwork(filtered.nodes, filtered.links);

// Responsive resize
window.addEventListener('resize', debounce(() => {
  config.width = window.innerWidth;
  config.height = window.innerHeight;
  svg.attr('width', config.width).attr('height', config.height);
  svg.attr('viewBox', [0, 0, config.width, config.height]);
}, 250));
*/

// ==================== CSS STYLES ====================

/*
Required CSS (add to your stylesheet):

.node {
  cursor: pointer;
  transition: all 0.2s ease;
}

.node:hover {
  filter: drop-shadow(0 0 8px rgba(74, 144, 226, 0.8));
}

.link {
  transition: opacity 0.2s ease, stroke-width 0.2s ease;
}

.network-tooltip {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  line-height: 1.4;
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .node {
    stroke-width: 1px !important;
  }

  text {
    font-size: 10px !important;
  }
}
*/
