<template>
  <div id="map-tests">
    <MglMap
      :accessToken="map_defaults.access_token"
      :mapStyle="map_defaults.map_style"
      :center="map_defaults.center"
      :zoom="map_defaults.zoom_level"
      @load="OnMapLoaded"
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
import axios from "axios";

export default {
  components: {
    MglMap,
    MglMarker,
    MglNavigationControl,
    MglGeojsonLayer
  },

  mounted() {
    console.log("Component mounted!");
  },

  methods: {
    OnMapLoaded(event) {
      // console.log(event.map.getLayer);
      // console.log(event.component.layer);

      // this.mapp = event.map;
      // this.$store.mapp = event.map;

      // event.map.flyTo({center: [13.516042572916149, 45.44681239419725], zoom:9})
    }
  },

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
          type: "FeatureCollection",
          id: "beaches_default_layer",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [13.9070370980641, 44.7860727950407]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [13.8990643980652, 44.817931095039]
              }
            }
          ]
        }
      },
      geoJsonLayer: {
        type: "circle",
        paint: {
          "circle-color": "#088"
        }
      },
      beaches: null,
      mapp: null
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
