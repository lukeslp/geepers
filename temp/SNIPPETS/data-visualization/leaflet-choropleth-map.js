"""
Leaflet.js Choropleth Map with Interactive Features

Description: Create an interactive choropleth map with Leaflet showing data density
by geographic regions. Includes hover effects, popups, info control, and legend.

Use Cases:
- Geographic data visualization (population, statistics, counts)
- Regional analysis and comparison
- Data-driven storytelling with maps

Dependencies:
- Leaflet.js (https://leafletjs.com/)
- GeoJSON data for boundaries
- OpenStreetMap tiles (or alternative tile provider)

Notes:
- Color scale based on data density
- Hover highlighting with visual feedback
- Information control shows details on hover
- Legend provides color scale reference
- Fully customizable color scheme

Related Snippets:
- See D3.js choropleth for alternative implementation
- See data-dashboard.js for integrating with other visualizations
"""

// Configuration
const dataByRegion = {
    "United States": 18,
    "China": 3,
    "France": 2,
    "India": 2,
    "Canada": 2,
    "Spain": 1,
    "Mexico": 1
};

// Initialize map
const map = L.map('map').setView([20, 0], 2);

// Add base tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18
}).addTo(map);

// Color scale function
function getColor(value) {
    return value > 10 ? '#800026' :
           value > 5  ? '#BD0026' :
           value > 2  ? '#E31A1C' :
           value > 1  ? '#FC4E2A' :
           value > 0  ? '#FD8D3C' :
                        '#FFEDA0';
}

// Style function for features
function style(feature) {
    const value = dataByRegion[feature.properties.ADMIN] || 0;
    return {
        fillColor: getColor(value),
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
    };
}

// Highlight feature on hover
function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 3,
        color: '#666',
        fillOpacity: 0.9
    });
    layer.bringToFront();
    info.update(layer.feature.properties);
}

// Reset highlight
function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

// Attach events to each feature
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });

    const value = dataByRegion[feature.properties.ADMIN] || 0;
    layer.bindPopup(
        `<strong>${feature.properties.ADMIN}</strong><br>` +
        `Value: ${value}`
    );
}

// Information control
const info = L.control();

info.onAdd = function () {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>Data Visualization</h4>' + (props ?
        `<b>${props.ADMIN}</b><br>Value: ${dataByRegion[props.ADMIN] || 0}` :
        'Hover over a region');
};

info.addTo(map);

// Legend control
const legend = L.control({position: 'bottomright'});

legend.onAdd = function () {
    const div = L.DomUtil.create('div', 'legend');
    const grades = [0, 1, 2, 5, 10];
    const labels = [];

    div.innerHTML += '<b>Value Range</b><br>';

    for (let i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

// Load and display GeoJSON
let geojson;
fetch('countries.geo.json')
    .then(response => response.json())
    .then(data => {
        geojson = L.geoJson(data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
    })
    .catch(error => console.error('Error loading GeoJSON:', error));

// Optional: Fit map to bounds of data
// map.fitBounds(geojson.getBounds());

/*
CSS Styling (add to your stylesheet):

.info {
    padding: 6px 8px;
    background: white;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
}

.info h4 {
    margin: 0 0 5px;
    color: #777;
}

.legend {
    line-height: 18px;
    color: #555;
    background: white;
    background: rgba(255,255,255,0.9);
    padding: 6px 8px;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

.legend i {
    width: 18px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.7;
}
*/
