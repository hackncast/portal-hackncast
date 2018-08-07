<template>
  <v-app dark id="app">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>
    <layout-broker :layouts="layouts" :current="$route.meta.layout"/>
    <toast />
    <form-errors />
  </v-app>
</template>

<script>
import layouts from '@/layouts'
import Toast from '@/plugins/toast/Toast'
import LayoutBroker from 'vue-layout-broker'
import FormErrors from '@/plugins/formerrors/FormErrors'

export default {
  name: 'App',

  components: { LayoutBroker, Toast, FormErrors },

  data () {
    return {
      layouts
    }
  }
}
</script>
