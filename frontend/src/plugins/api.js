const requireComponent = require.context('@/api/', false, /\.js$/)

const apiFactory = axios => {
  const apis = {}
  requireComponent.keys().forEach(fname => {
    let name = fname.replace('.js', '').replace('./', '')
    apis[name] = requireComponent(fname).default(axios)
  })

  return apis
}

export default {
  install (Vue, options) {
    const api = apiFactory(Vue.axios)
    Vue.api = api
    Vue.prototype.$api = api
  }
}
