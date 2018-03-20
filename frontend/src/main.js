// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

// External Plugins
import Vuetify from 'vuetify'
import VueHead from 'vue-head'
import VueMoment from 'vue-moment'
import VueResource from 'vue-resource'
import VeeValidate from 'vee-validate'
import Transitions from 'vue2-transitions'
import vueTopprogress from 'vue-top-progress'

// Styling
import '@/style/base.sass'

// My plugins and modules
import App from '@/App'
import router from '@/router'
import VueLodash from '@/plugins/VueLodash'
import VueCookies from '@/plugins/VueCookies'
import VuetifyToasts from '@/plugins/VuetifyToasts'
import Progress from '@/plugins/Progress'
import { store } from '@/store/store'

Vue.use(Vuetify)
Vue.use(VueHead)
Vue.use(VueLodash)
Vue.use(VueMoment)
Vue.use(VueCookies)
Vue.use(VueResource)
Vue.use(VeeValidate)
Vue.use(Transitions)
Vue.use(VuetifyToasts)
Vue.use(vueTopprogress)
Vue.use(Progress)

Vue.config.productionTip = false

Vue.http.interceptors.push(function (request, next) {
  let csrftoken = Vue.cookies.get('csrftoken')
  if (request.method !== 'GET' && request.method !== 'OPTION' && csrftoken !== undefined) {
    request.headers.set('X-CSRFToken', csrftoken)
  }
  next()
})

Vue.http.interceptors.push(function (request, next) {
  next((response) => {
    if (response.body && response.body.django_messages) {
      for (let message of response.body.django_messages) {
        Vue.toasts.open({
          text: message.message,
          type: message.level_tag
        })
      }
      delete response.body.django_messages
    }
  })
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
