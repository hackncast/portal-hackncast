// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

// External Plugins
import Vuetify from 'vuetify'
import VueI18n from 'vue-i18n'
import VueHead from 'vue-head'
import VueMoment from 'vue-moment'
import VueResource from 'vue-resource'
import VeeValidate from 'vee-validate'
import Transitions from 'vue2-transitions'
import vueTopprogress from 'vue-top-progress'

// Styling
import '@/style/base.sass'

// My plugins and modules
import messages from '@/i18n'
import App from '@/App'
import router from '@/router'
import VueLodash from '@/plugins/VueLodash'
import VueCookies from '@/plugins/VueCookies'
import VuetifyToasts from '@/plugins/VuetifyToasts'
import Progress from '@/plugins/Progress'
import { store } from '@/store/store'

Vue.use(Vuetify)
Vue.use(VueI18n)
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
    if (response.ok === false && (response.status >= 500 && response.status <= 505)) {
      setTimeout(() => {
        Vue.toasts.open({
          text: 'An error ocurred while quering the server, please check your internet connection and try again later.',
          type: 'error',
          persist: true
        })
      }, 1000)
    }

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

const i18n = new VueI18n({
  locale: localStorage.getItem('language') || navigator.language || navigator.languages[0],
  messages
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  components: { App },
  template: '<App/>'
})
