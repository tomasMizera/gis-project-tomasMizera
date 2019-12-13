mapboxgl.accessToken = 'pk.eyJ1IjoidG9tYXNtaXplcmEiLCJhIjoiY2syNjYwZWU4MDM1eTNqbWpzeHFtbndyeSJ9.jUjn1KiL9fLH3rm8cTOL3A';
var map = new mapboxgl.Map({
    container: 'map',
    zoom: 6,
    center: [16.040558978480476, 44.856239137871034],
    style: 'mapbox://styles/tomasmizera/ck26ikzn01ubj1cpo9aq9k537'
});

map.on('mousemove', function (e) {
    document.getElementById('mouse').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        JSON.stringify(e.point) + '<br />' +
        // e.lngLat is the longitude, latitude geographical position of the event
        JSON.stringify(e.lngLat.wrap());
});


map.on("load", function () {
    // Add zoom and rotation controls to the map.
    // map.addControl(new mapboxgl.NavigationControl());

    let url = 'http://localhost:5000/api/get_beaches';
    $.get(url, (data, status) => {

        // https://i.imgur.com/MK4NUzI.png
        map.loadImage("https://img.icons8.com/metro/26/000000/marker.png", function (error, image) {
            if (error) throw error;
            map.addImage("beaches", image);

            /* Style layer: A style layer ties together the source and image and specifies how they are displayed on the map. */
            map.addLayer({
                id: "beaches",
                type: "symbol",
                /* Source: A data source specifies the geographic coordinate where the image marker gets placed. */
                source: {
                    type: "geojson",
                    data: data
                },
                layout: {
                    "icon-image": "beaches",
                }
            });
        });
    });
});

$('#sights_visible').change((event) => {
    if (event.target.checked) {
        if (map.getSource('sights') == undefined) {
            url = 'http://localhost:5000/api/get_sight_views'
            $.get(url, (data, status) => {
                map.addLayer({
                    'id': "sights",
                    'type': "fill",
                    'source': {
                        'type': 'geojson',
                        'data': data
                    },
                    'paint': {
                        'fill-color': '#088',
                        'fill-opacity': 0.5
                    }
                })
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
            $.get(url, (data, status) => {
                console.log(data);
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
