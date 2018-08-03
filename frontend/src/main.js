import Vue from 'vue'
import App from './App.vue'
import routes from './routes'
import store from './store'

import '@babel/polyfill'

// Styling
import 'vuetify/dist/vuetify.min.css'
import '@/style/base.sass'

// Plugins
import './plugins'

Vue.config.productionTip = false

new Vue({
  router: routes,
  store,
  render: h => h(App)
}).$mount('#app')
