import lodash from 'lodash'

const VueLodash = {
  install (Vue, options) {
    Vue.lodash = lodash
    Vue.prototype.$lodash = lodash
  }
}

export default VueLodash
