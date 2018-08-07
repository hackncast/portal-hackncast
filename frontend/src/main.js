import Vue from 'vue'

import App from './App.vue'
import router from './routes'
import store from './store'

import '@babel/polyfill'

// Styling
import 'vuetify/dist/vuetify.min.css'
import '@/style/base.sass'

// Plugins
import './plugins'

Vue.config.productionTip = false

window.Vue = new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
