<template>
  <div id="app">
    <ScenarioView msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import ScenarioView from './components/ScenarioView.vue'

export default {
  name: 'App',
  components: {
    ScenarioView
  }
}
</script>

<style>
body {
  margin : 0;
  padding : 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

</style>
