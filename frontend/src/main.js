// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

// External Plugins
import Vuetify from 'vuetify'
import VueHead from 'vue-head'
import VueMoment from 'vue-moment'
import VueResource from 'vue-resource'
import Transitions from 'vue2-transitions'
import vueTopprogress from 'vue-top-progress'
import VeeValidate from 'vee-validate'

// Styling
import '@/style/base.sass'

// My plugins and modules
import App from '@/App'
import router from '@/router'
import Api from '@/plugins/Api'
import VueLodash from '@/plugins/VueLodash'
import VueCookies from '@/plugins/VueCookies'
import VuetifyToasts from '@/plugins/VuetifyToasts'
import VueUA from '@/plugins/VueUA'
import Progress from '@/plugins/Progress'
import { store } from '@/store/store'
import models from '@/models'

// Localization
import I18n from '@/i18n'
const i18n = I18n.init(Vue)

models.initialize()

// Vue Plugins Initialization
Vue.use(VueUA)
Vue.use(Vuetify)
Vue.use(VueHead)
Vue.use(Progress)
Vue.use(VueLodash)
Vue.use(VueMoment)
Vue.use(VueCookies)
Vue.use(VueResource)
Vue.use(Transitions)
Vue.use(VuetifyToasts)
Vue.use(vueTopprogress)
Vue.use(VeeValidate, { locale: I18n.veeValidateLocale })
Vue.use(Api)

Vue.config.productionTip = false

// Interceptors
Vue.http.interceptors.push(function (request, next) {
  // CSRF Token on POST, PUSH, DELETE and etc
  let csrftoken = Vue.cookies.get('csrftoken')
  if (request.method !== 'GET' && request.method !== 'OPTION' && csrftoken !== undefined) {
    request.headers.set('X-CSRFToken', csrftoken)
  }
  next()
})

Vue.http.interceptors.push(function (request, next) {
  // Automatic messages on response
  next((response) => {
    if (response.ok === false && (response.status >= 500 && response.status <= 505)) {
      setTimeout(() => {
        Vue.toasts.open({
          text: i18n.t('message.server-error'),
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

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  components: { App },
  template: '<App/>'
})
