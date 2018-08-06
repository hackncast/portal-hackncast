<template>
  <v-app dark id="app">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>
    <layout-broker :layouts="layouts" :current="$route.meta.layout"/>
    <toast />
  </v-app>
</template>

<script>
import layouts from '@/layouts'
import LayoutBroker from 'vue-layout-broker'
import Toast from '@/plugins/toast/Toast'

export default {
  name: 'App',

  components: { LayoutBroker, Toast },

  data () {
    return {
      layouts
    }
  }
}
</script>
