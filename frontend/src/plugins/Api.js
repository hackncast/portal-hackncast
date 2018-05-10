import apiUrls from '@/apiUrls'
import { Resource } from 'vue-resource'

let api
let methods = {
  partialUpdate: {method: 'PATCH'},
  peak: {method: 'HEAD'},
  options: {method: 'OPTIONS'}
}

function __buildResources (resources) {
  let context = {}
  for (let entry of resources) {
    let resource = Resource(entry.url, {}, methods)

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
  constructor () {
    if (!api) {
      api = this
    } else {
      return api
    }

    for (let contextName of Object.keys(apiUrls)) {
      this[contextName] = __buildResources(apiUrls[contextName])
    }
    return api
  }
}

const Api = {
  install (Vue, options) {
    if (!api) {
      api = new ApiHelper()
    }
    Vue.prototype.$api = api
    Vue.api = api
  }
}

export default Api
export { ApiHelper }
