import UA from 'ua-parser-js'

const VueUA = {
  install (Vue, options) {
    Vue.ua = UA
    Vue.prototype.$ua = UA
  }
}

export default VueUA
