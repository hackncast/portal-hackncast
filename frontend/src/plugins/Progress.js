import { UI } from '@/store/mutation-types'
import { store } from '@/store/store'

const progress = {
  start () { store.commit(UI.PROGRESS_START) },
  stop () { store.commit(UI.PROGRESS_STOP) },
  fail () { store.commit(UI.PROGRESS_FAIL) }
}

const Progress = {
  install (Vue, options) {
    Vue.prototype.$progress = progress
    Vue.progress = progress
  }
}

export default Progress
