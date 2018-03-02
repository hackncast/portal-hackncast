import { UI } from '@/store/mutation-types'

export default {
  state: {
    darkTheme: (localStorage.getItem('UI_DarkTheme') === 'true'),
    sidebarVisible: false
  },

  mutations: {
    [UI.DARK_THEME] (state, value) {
      state.darkTheme = value
      localStorage.setItem('UI_DarkTheme', value)
    },
    [UI.SIDEBAR_VISIBLE] (state, visible) {
      state.sidebarVisible = visible
    }
  }
}
