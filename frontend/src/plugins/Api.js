let api
let methods = {
  partialUpdate: {method: 'PATCH'},
  peak: {method: 'HEAD'},
  options: {method: 'OPTIONS'}
}

function __buildResources (vue, resources) {
  let context = {}
  for (let entry of resources) {
    let resource = vue.resource(entry.url, {}, methods)

    if (entry.methods) {
      if (entry.methods.indexOf('GET') < 0) {
        delete resource.get
        delete resource.query
      }

      if (entry.methods.indexOf('POST') < 0) {
        delete resource.save
      }

      if (entry.methods.indexOf('PUT') < 0) {
        delete resource.update
      }

      if (entry.methods.indexOf('DELETE') < 0) {
        delete resource.remove
        delete resource.delete
      }

      if (entry.methods.indexOf('PATCH') < 0) {
        delete resource.partialUpdate
      }
    }
    context[entry.name] = resource
  }
  return context
}

class ApiHelper {
  constructor (vue) {
    if (!api) {
      api = this
      this.vue = vue
    } else {
      return api
    }

    vue.http.get('/api/')
      .then(data => data.json())
      .then(data => {
        for (let contextName of Object.keys(data)) {
          if (contextName === 'django_messages') continue
          this[contextName] = __buildResources(vue, data[contextName])
        }
      })
    return api
  }
}

const Api = {
  install (Vue, options) {
    if (!api) {
      api = new ApiHelper(Vue)
    }
    Vue.prototype.$api = api
    Vue.api = api
  }
}

export default Api
export { ApiHelper }
