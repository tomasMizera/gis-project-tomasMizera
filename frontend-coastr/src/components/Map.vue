<template>
  <div id="map-tests">
    <MglMap
      :accessToken="map_defaults.access_token"
      :mapStyle="map_defaults.map_style"
      :center="map_defaults.center"
      :zoom="map_defaults.zoom_level"
    >
      <MglNavigationControl position="top-right" />
      <MglMarker :coordinates="map_layers.markers.test_point_geo" anchor="center" />
      <MglGeojsonLayer
        :sourceId="geoJsonSource.data.id"
        :source="geoJsonSource"
        :layer="geoJsonLayer"
        layerId="ds"
      />
    </MglMap>
  </div>
</template>

<script>
import Mapbox from "mapbox-gl";
import {
  MglMap,
  MglNavigationControl,
  MglMarker,
  MglGeojsonLayer
} from "vue-mapbox";

export default {
  components: {
    MglMap,
    MglMarker,
    MglNavigationControl,
    MglGeojsonLayer
  },

  mounted() {
    console.log(this.mapbox.Map);
  },

  methods: {},

  data() {
    // LONG, LAT!
    return {
      map_defaults: {
        access_token:
          "pk.eyJ1IjoidG9tYXNtaXplcmEiLCJhIjoiY2syNjYwZWU4MDM1eTNqbWpzeHFtbndyeSJ9.jUjn1KiL9fLH3rm8cTOL3A",
        map_style: "mapbox://styles/tomasmizera/ck26ikzn01ubj1cpo9aq9k537",
        center: [16.040558978480476, 44.856239137871034],
        zoom_level: 6
      },
      map_layers: {
        markers: {
          test_point_geo: [13.516042572916149, 45.44681239419725]
        }
      },
      geoJsonSource: {
        type: "geojson",
        data: {
          id: "thisIsMySource",
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Polygon",
                coordinates: [
                  [
                    [13.451385498046875, 45.10357701164311],
                    [13.250885009765625, 44.921056574907226],
                    [13.6395263671875, 44.896741421341964],
                    [13.726043701171875, 45.02792105147572],
                    [13.451385498046875, 45.10357701164311]
                  ]
                ]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Polygon",
                coordinates: [
                  [
                    [13.503570556640625, 45.24878781698633],
                    [13.326416015624998, 45.12295984719159],
                    [13.50494384765625, 45.03956694724904],
                    [13.742523193359373, 45.22461173085719],
                    [13.503570556640625, 45.24878781698633]
                  ]
                ]
              }
            }
          ]
        }
      },
      geoJsonLayer: {
        type: "fill",
        paint: {
          "fill-color": "#088",
          "fill-opacity": 0.8
        }
      }
    };
  },

  created() {
    // We need to set mapbox-gl library here in order to use it in template
    this.mapbox = Mapbox;
  }
};
</script>

<style>
/* @import "../../node_modules/mapbox-gl/dist/mapbox-gl.css"; */

.mgl-map-wrapper {
  height: 750px;
}
</style>


// http://localhost:5000/get_view_locations
