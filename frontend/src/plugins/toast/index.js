import store from '@/store'
import toastStore from './store'

store.registerModule('toast', toastStore)

function toastDispatcher (options) { store.dispatch('toast/toast', options) }

export default {
  install (Vue, options) {
    Vue.toast = toastDispatcher
    Vue.prototype.$toast = toastDispatcher
  }
}
