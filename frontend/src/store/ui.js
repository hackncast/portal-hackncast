const NAVBAR_LIGHT_COLOR = 'blue accent-2'
const NAVBAR_DARK_COLOR = 'blue-grey darken-3'
const BACKGROUND_DARK_COLOR = 'darkBackground'
const BACKGROUND_LIGHT_COLOR = 'grey lighten-3'

export const state = () => ({
  progressStatus: 'stop',
  darkTheme: (localStorage.getItem('UI_DarkTheme') === 'true'),
  miniSidebar: (localStorage.getItem('UI_MiniSidebar') === 'true'),
  sidebarVisible: false,
  uiSettingsVisible: false
})

export const getters = {
  progressBarStatus: state => state.progressStatus,
  navbarColor: state => state.darkTheme ? NAVBAR_DARK_COLOR : NAVBAR_LIGHT_COLOR,
  backgroundColor: state => state.darkTheme ? BACKGROUND_DARK_COLOR : BACKGROUND_LIGHT_COLOR,
  chromeColor: state => state.darkTheme ? '#263238' : '#2962FF'
}

export const mutations = {
  DARK_THEME (state, value) {
    state.darkTheme = value
    localStorage.setItem('UI_DarkTheme', value)
  },
  MINI_SIDEBAR (state, value) {
    state.miniSidebar = value
    localStorage.setItem('UI_MiniSidebar', value)
  },
  SIDEBAR_VISIBLE (state, value) { state.sidebarVisible = value },
  PROGRESS_START (state) { state.progressStatus = 'start' },
  PROGRESS_STOP (state) { state.progressStatus = 'stop' },
  PROGRESS_FAIL (sate) { state.progressStatus = 'fail' }
}

export const actions = {
  startProgressBar ({commit}) { commit('PROGRESS_START') },
  endProgressBar ({commit}) { commit('PROGRESS_STOP') },
  failProgressBar ({commit}) { commit('PROGRESS_FAIL') },
  setDarkTheme ({commit}, value) { commit('DARK_THEME', value) },
  showSidebar ({commit}, value) { commit('SIDEBAR_VISIBLE', value) },
  setMiniSidebar ({commit}, value) { commit('MINI_SIDEBAR', value) }
}
