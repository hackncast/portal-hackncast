export const state = () => ({
  progressStatus: 'stop',
  darkTheme: (localStorage.getItem('UI_DarkTheme') === 'true'),
  sidebarVisible: false,
  uiSettingsVisible: false
})

export const getters = {
  progressBarStatus: state => state.progressStatus
}

export const mutations = {
  DARK_THEME (state, value) {
    state.darkTheme = value
    localStorage.setItem('UI_DarkTheme', value)
  },

  PROGRESS_START (state) { state.progressStatus = 'start' },
  PROGRESS_STOP (state) { state.progressStatus = 'stop' },
  PROGRESS_FAIL (state) { state.progressStatus = 'fail' }
}

export const actions = {
  startProgressBar ({commit}) { commit('PROGRESS_START') },
  endProgressBar ({commit}) { commit('PROGRESS_STOP') },
  failProgressBar ({commit}) { commit('PROGRESS_FAIL') },
  setDarkTheme ({commit}, value) { commit('DARK_THEME', value) }
}
