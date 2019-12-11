<template>
  <div id="app">
    <Intro/>
    <Map/>
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
import Map from './components/Map.vue'
import Intro from './components/Intro.vue'

export default {
  name: 'app',
  components: {
    Intro,
    Map
  }
}
</script>
