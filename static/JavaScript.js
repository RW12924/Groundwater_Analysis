var data = [];  // This will be populated with actual data

// Sample initialization for Leaflet map
var map = L.map('leaflet-map').setView([37.5, -119], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Function to update maps with filtered data
function updateMaps(selectedYear) {
    console.log('Selected Year:', selectedYear);

    // Fetch data if not already done
    if (data.length === 0) {
        fetch('/data')
            .then(response => response.json())
            .then(jsonData => {
                data = JSON.parse(jsonData);  // response.json() already parses the JSON
                filterAndRender(selectedYear);
            })
            .catch(error => console.error('Error fetching data:', error));
    } else {
        filterAndRender(selectedYear);
    }
}

function filterAndRender(selectedYear) {
    var filteredData = data.filter(d => d['year'].toString() === selectedYear.toString());
    console.log('Filtered Data:', filteredData);

    // Update Plotly map
    var layout = {
        title: {
            text: 'California Groundwater Map',
            x: 0.5,
            xanchor: 'center'
        },
        geo: {
            scope: 'usa',
            projection: {
                type: 'albers usa'
            },
            center: {
                lat: 37.5,
                lon: -119
            },
            showland: true,
            landcolor: '#f4f4f4',
            lataxis: { range: [32, 42] },
            lonaxis: { range: [-125, -114] }
        },
        margin: {
            l: 50,
            r: 50,
            t: 90,
            b: 0
        },
        height: 500,
        width: '100%'
    };
    var data_layers = [
        {
            type: 'scattergeo',
            mode: 'markers',
            lon: filteredData.map(d => parseFloat(d.longitude)),
            lat: filteredData.map(d => parseFloat(d.latitude)),
            text: filteredData.map(d => `Site Code: ${d['site_code']}, Measurement Date: ${d['year']}`),
            marker: {
                size: 10,
                color: filteredData.map(d => parseFloat(d['gse'])),
                colorscale: 'Viridis',
                colorbar: {
                    title: 'Groundwater Elevation'
                }
            }
        }
    ];
    Plotly.newPlot('plotly-map', data_layers, layout);

    // Clear existing markers and heatmap on Leaflet map
    map.eachLayer(function(layer) {
        if (!(layer instanceof L.TileLayer)) {
            map.removeLayer(layer);
        }
    });

    // Create new markers and heatmap based on filtered data
    var markers = L.layerGroup();
    var heatData = [];
    filteredData.forEach(d => {
        // Create markers
        var markerOptions = {
            radius: 8,
            fillColor: getColor(d.well_use),
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: getFillOpacity(d.well_use)
        };
        var marker = L.circleMarker([parseFloat(d.latitude), parseFloat(d.longitude)], markerOptions)
            .bindPopup(`Site Code: ${d['site_code']}<br>Measurement Date: ${d['year']}`);
        markers.addLayer(marker);

        // Add data for heatmap
        if (d.well_use === 'Good' || d.well_use === 'Questionable' || d.well_use === 'Provisional') {
            heatData.push([parseFloat(d.latitude), parseFloat(d.longitude)]);
        }
    });
    markers.addTo(map);
    L.heatLayer(heatData, {radius: 20, blur: 15, maxZoom: 10}).addTo(map);
}

function getColor(well_use) {
    switch (well_use) {
        case 'Good':
            return 'green';
        case 'Questionable':
            return 'red';
        case 'Provisional':
            return 'grey';
        case 'Missing':
            return 'transparent';
        default:
            return 'black'; // Fallback color
    }
}

function getFillOpacity(well_use) {
    return well_use === 'Missing' ? 0 : 0.8;
}

// Initial map update with the first year in the dropdown
document.addEventListener('DOMContentLoaded', function () {
    var initialYear = document.getElementById('year-dropdown').value;
    updateMaps(initialYear);
});
