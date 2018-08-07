import store from '@/store'
import formerrorStore from './store'

store.registerModule('formerrors', formerrorStore)

function formErrorsDispatcher (errors) { store.dispatch('formerrors/show', errors) }

export default {
  install (Vue, options) {
    Vue.formErrors = formErrorsDispatcher
    Vue.prototype.$formErrors = formErrorsDispatcher
  }
}
