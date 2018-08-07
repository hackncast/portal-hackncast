import store from '@/store'
import Cookies from 'js-cookie'

function injectCSRFToken (config) {
  if (process.env.VUE_APP_DEBUG === 'true') {
    console.log('Request to: ' + config.url)
  }

  const csrftoken = Cookies.get('csrftoken')
  if (csrftoken !== undefined) {
    config.headers.common['X-CSRFToken'] = csrftoken
  }
  return config
}

function startProgressBar (config) {
  store.dispatch('ui/startProgressBar')
  return config
}

function endProgressBar (response) {
  store.dispatch('ui/endProgressBar')
  return response
}

function failProgressBar (error) {
  store.dispatch('ui/failProgressBar')
  return Promise.reject(error)
}

export default {
  install (Vue, options) {
    Vue.axios.interceptors.request.use(injectCSRFToken)
    Vue.axios.interceptors.request.use(startProgressBar)

    Vue.axios.interceptors.response.use(
      endProgressBar, failProgressBar
    )
  }
}