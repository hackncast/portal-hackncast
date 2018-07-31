import Cookies from 'js-cookie'

const VueCookies = {
  install (Vue, options) {
    Vue.prototype.$cookies = Cookies
    Vue.cookies = Cookies
  }
}

export default VueCookies
