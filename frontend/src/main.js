import Vue from 'vue'
import App from './App.vue'
import routes from './routes'
import store from './store'

import plugins from './plugins'
plugins.install(Vue)

Vue.config.productionTip = false

new Vue({
  router: routes,
  store,
  render: h => h(App)
}).$mount('#app')
