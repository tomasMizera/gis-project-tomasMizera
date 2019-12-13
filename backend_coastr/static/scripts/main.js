var slider = document.getElementById("walk-range");
var apply = document.getElementById("apply-filters");
var output = document.getElementById("slider-val");
output.innerHTML = "allow intersections";

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
    output.innerHTML = this.value / 400 + ' km';
}

mapboxgl.accessToken = 'pk.eyJ1IjoidG9tYXNtaXplcmEiLCJhIjoiY2syNjYwZWU4MDM1eTNqbWpzeHFtbndyeSJ9.jUjn1KiL9fLH3rm8cTOL3A';
var map = new mapboxgl.Map({
    container: 'map',
    zoom: 6,
    center: [16.040558978480476, 44.856239137871034],
    style: 'mapbox://styles/tomasmizera/ck26ikzn01ubj1cpo9aq9k537'
});

map.on('mousemove', function (e) {
    document.getElementById('mouse').innerHTML =
        JSON.stringify(e.point) + '<br />' +
        JSON.stringify(e.lngLat.wrap());
});

map.on("load", function () {
    $("slider-val").text("0.05")

    let url = 'http://localhost:5000/api/get_beaches';
    $.get(url, (data, status) => {

        map.loadImage("https://img.icons8.com/android/24/000000/beach.png", function (error, image) {
            if (error) throw error;
            map.addImage("beaches", image);

            map.addLayer({
                id: "beaches",
                type: "symbol",
                source: {
                    type: "geojson",
                    data: data
                },
                layout: {
                    "icon-image": "beaches"
                }
            });
        });
    });

    map.on('click', 'beaches', function (e) {
        var coordinates = e.lngLat;
        var name = e.features[0].properties.name;

        if (name == "null") {
            name = "Uknown name"
        }

        map.flyTo({
            center: coordinates,
            zoom: 9
        })
        
        new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(name)
        .addTo(map);

        
    });

    map.on('mouseenter', 'beaches', function () {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'beaches', function () {
        map.getCanvas().style.cursor = '';
    });
});

$('#sights_visible').change((event) => {
    if (event.target.checked) {
        if (map.getSource('sights') == undefined) {
            console.info('Fetching sight views');
            url = 'http://localhost:5000/api/get_sight_views'
            $.get(url, (data, status) => {
                console.info('Sight views fetched');
                map.addLayer({
                    'id': "sights",
                    'type': "fill",
                    'source': {
                        'type': 'geojson',
                        'data': data
                    },
                    'paint': {
                        'fill-color': '#880',
                        'fill-opacity': 0.5
                    }
                }, "beaches")
            });
        } else {
            map.setLayoutProperty('sights', 'visibility', 'visible');
        }
    } else {
        map.setLayoutProperty('sights', 'visibility', 'none');
    }
});

$('#show_coastline').change((event) => {
    if (event.target.checked) {
        if (map.getSource('coastline') == undefined) {
            url = 'http://localhost:5000/api/get_coastline'
            console.info('Fetching coastlines')
            $.get(url, (data, status) => {
                console.info('Coastlines fetched');
                map.addLayer({
                    'id': "coastline",
                    'type': "line",
                    'source': {
                        'type': 'geojson',
                        'data': data
                    },
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#088',
                        'line-width': 7
                    }
                }, "beaches")
            });
        } else {
            map.setLayoutProperty('coastline', 'visibility', 'visible');
        }
    } else {
        map.setLayoutProperty('coastline', 'visibility', 'none');
    }
});

$('#apply-filters').click(() => {
    if (!!map.getLayer('intersections')) {
        map.removeLayer('intersections')
        map.removeSource('intersections')
    }
    url = 'http://localhost:5000/api/get_intersections'
    console.info('Fetching intersections')
    $.get(url, { walking_distance: slider.value / 400 }, (data, status) => {
        console.info('intersections fetched');
        map.addLayer({
            'id': "intersections",
            'type': "fill",
            'source': {
                'type': 'geojson',
                'data': data
            },
            'paint': {
                'fill-color': '#808',
                'fill-opacity': 0.5
            }
        })
    });
})

$('#show-intersections').change((event) => {
    if (event.target.checked) {
        slider.disabled = false;
        apply.disabled = false;
        output.innerHTML = slider.value / 400 + ' km';
        if (map.getSource('intersections') == undefined) {
            url = 'http://localhost:5000/api/get_intersections'
            console.info('Fetching intersections')
            $.get(url, { walking_distance: slider.value / 400 }, (data, status) => {
                console.info('intersections fetched');
                map.addLayer({
                    'id': "intersections",
                    'type': "fill",
                    'source': {
                        'type': 'geojson',
                        'data': data
                    },
                    'paint': {
                        'fill-color': '#808',
                        'fill-opacity': 0.5
                    }
                })
            });
        } else {
            map.setLayoutProperty('intersections', 'visibility', 'visible');
        }
    } else {
        slider.disabled = true;
        output.innerHTML = 'allow intersections'
        apply.disabled = true;
        map.setLayoutProperty('intersections', 'visibility', 'none');
    }
});