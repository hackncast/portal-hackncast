import { UI } from '@/store/mutation-types'

export default {
  state: {
    lightTheme: true,
    sidebarVisible: false
  },

  mutations: {
    [UI.LIGHT_THEME] (state, value) {
      state.lightTheme = value
    },
    [UI.SIDEBAR_VISIBLE] (state, visible) {
      state.sidebarVisible = visible
    }
  }
}
