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
            let url = 'http://localhost:5000/api/get_beaches';
            $.get(url, (data, status) => {

                // https://i.imgur.com/MK4NUzI.png
                map.loadImage("https://img.icons8.com/metro/26/000000/marker.png", function (error, image) {
                    if (error) throw error;
                    map.addImage("beaches", image);
                    /* Style layer: A style layer ties together the source and image and specifies how they are displayed on the map. */
                    map.addLayer({
                        id: "markers",
                        type: "symbol",
                        /* Source: A data source specifies the geographic coordinate where the image marker gets placed. */
                        source: {
                            type: "geojson",
                            data: {
                                type: 'FeatureCollection',
                                features: data
                            }
                        },
                        layout: {
                            "icon-image": "beaches",
                        }
                    });
                });
            });

            url = 'http://localhost:5000/get_polygons';
            $.get(url, (data, status) => {
                map.addLayer({
                    'id': 'polygon',
                    'type': 'fill',
                    'source': {
                        'type': 'geojson',
                        'data': {
                            'type': 'Feature',
                            'geometry': {
                                'type': 'MultiPolygon',
                                'coordinates': data
                            }
                        }
                    },
                    'layout': {},
                    'paint': {
                        'fill-color': '#088',
                        'fill-opacity': 0.5
                    }
                });
            });
        });