<template>
  <div id="map-tests">
    <h1> Coastr Map</h1>
    <MglMap :accessToken="accessToken" :mapStyle="mapStyle" />
    <p> After map </p>
  </div>
</template>

<script>
import Mapbox from "mapbox-gl";
import { MglMap } from "vue-mapbox";

export default {
  components: {
    MglMap
  },
  data() {
    return {
      accessToken: "pk.eyJ1IjoidG9tYXNtaXplcmEiLCJhIjoiY2syNjYwZWU4MDM1eTNqbWpzeHFtbndyeSJ9.jUjn1KiL9fLH3rm8cTOL3A",
      mapStyle: "mapbox://styles/tomasmizera/ck26ikzn01ubj1cpo9aq9k537"
    };
  },

  created() {
    // We need to set mapbox-gl library here in order to use it in template
    this.mapbox = Mapbox;
  }
};
</script>

<style>
.mgl-map-wrapper {
  height: 750px;
}
</style>