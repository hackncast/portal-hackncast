import { UI } from '@/store/mutation-types'

export default {
  state: {
    sidebarVisible: false
  },

  mutations: {
    [UI.SIDEBAR_VISIBLE] (state, visible) {
      state.sidebarVisible = visible
    }
  }
}
