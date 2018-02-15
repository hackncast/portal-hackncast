// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from '@/router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

// External Plugins
import VueResource from 'vue-resource'
import VeeValidate from 'vee-validate'

// My plugins
import VueLodash from '@/plugins/VueLodash'

Vue.use(Vuetify)
Vue.use(VueLodash)
Vue.use(VueResource)
Vue.use(VeeValidate)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
