<template>
  <v-app dark id="app">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>
    <layout-broker :layouts="layouts" :current="$route.meta.layout"/>
  </v-app>
</template>

<script>
import layouts from '@/layouts'
import LayoutBroker from 'vue-layout-broker'

export default {
  name: 'App',

  components: { LayoutBroker },

  data () {
    return {
      layouts
    }
  }
}
</script>
