import Vue from 'vue'
import axios from 'axios'
import Vuetify from 'vuetify'
import VueHead from 'vue-head'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import VeeValidate from 'vee-validate'
import TopProgress from 'vue-top-progress'

// Pending
// import Transitions from 'vue2-transitions'

const instance = axios.create({
  baseURL: '/api/'
})

Vue.use(VueHead)
Vue.use(Vuetify)
Vue.use(VueMoment)
Vue.use(Vuetify, {})
Vue.use(TopProgress)
Vue.use(VeeValidate)
Vue.use(VueAxios, instance)

const requireModule = require.context('.', true, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return
  const plugin = requireModule(fileName).default

  if (plugin) {
    Vue.use(plugin)
  }
})
