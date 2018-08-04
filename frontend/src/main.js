import Vue from 'vue'
import Router from 'vue-router'

import App from './App.vue'
import routes from './routes'
import store from './store'

import '@babel/polyfill'

// Styling
import 'vuetify/dist/vuetify.min.css'
import '@/style/base.sass'

// Plugins
import './plugins'

Vue.use(Router)

Vue.config.productionTip = false

window.Vue = new Vue({
  store,
  render: h => h(App),
  router: new Router({
    mode: 'history',
    routes: routes,
    base: process.env.BASE_URL ? process.env.BASE_URL : undefined
  })
}).$mount('#app')
