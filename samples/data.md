[https://www.openstreetmap.org/export#map=8/44.596/14.705](https://www.openstreetmap.org/export#map=8/44.596/14.705)

download **Croatia** and show places, where you can enjoy open sea view (and sunset :) ) 

[https://en.wikipedia.org/wiki/Horizon](https://en.wikipedia.org/wiki/Horizon)
average person can see from shore to the distance of ~4km: `sqrt(13 * (your height in m))` km

API should return `GeoJson` format: [https://geojson.org/](https://geojson.org/)


```javascript
<script src='https://api.mapbox.com/mapbox-gl-js/v1.4.1/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v1.4.1/mapbox-gl.css' rel='stylesheet' />
```


```html
<div id='map' style='width: 400px; height: 300px;'></div>
<script>
mapboxgl.accessToken = 'pk.eyJ1IjoidG9tYXNtaXplcmEiLCJhIjoiY2syNjYwZWU4MDM1eTNqbWpzeHFtbndyeSJ9.jUjn1KiL9fLH3rm8cTOL3A';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11'
});
</script>
```
