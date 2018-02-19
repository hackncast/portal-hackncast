// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from '@/App'
import router from '@/router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

import VueResource from 'vue-resource'

import VueCookies from '@/plugins/VueCookies'
import { store } from '@/store/store'

Vue.use(Vuetify)
Vue.use(VueResource)
Vue.use(VueCookies)

Vue.config.productionTip = false

Vue.http.interceptors.push(function (request, next) {
  let csrftoken = Vue.cookies.get('csrftoken')
  if (request.method === 'POST' && csrftoken !== undefined) {
    request.headers.set('X-CSRFToken', csrftoken)
  }
  next()
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
