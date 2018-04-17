import { UI } from '@/store/mutation-types'
import I18n from '@/i18n'

const NAVBAR_LIGHT_COLOR = 'blue accent-2'
const NAVBAR_DARK_COLOR = 'blue-grey darken-3'
const BACKGROUND_DARK_COLOR = 'darkBackground'
const BACKGROUND_LIGHT_COLOR = 'grey lighten-3'

export default {
  state: {
    darkTheme: (localStorage.getItem('UI_DarkTheme') === 'true'),
    navbarColor: (localStorage.getItem('UI_DarkTheme') === 'true') ? NAVBAR_DARK_COLOR : NAVBAR_LIGHT_COLOR,
    backgroundColor: (localStorage.getItem('UI_DarkTheme') === 'true') ? BACKGROUND_DARK_COLOR : BACKGROUND_LIGHT_COLOR,
    language: I18n.locale,
    sidebarVisible: false,
    progressStatus: false
  },

  getters: {
    getChromeColor: state => state.darkTheme ? '#263238' : '#2962FF'
  },

  mutations: {
    [UI.DARK_THEME] (state, value) {
      state.darkTheme = value
      localStorage.setItem('UI_DarkTheme', value)
      state.navbarColor = value ? NAVBAR_DARK_COLOR : NAVBAR_LIGHT_COLOR
      state.backgroundColor = value ? BACKGROUND_DARK_COLOR : BACKGROUND_LIGHT_COLOR
      state.chromeColor = '#2e2e2e'
    },
    [UI.NAVBAR_COLOR] (state, color) {
      state.navbarColor = color
    },
    [UI.SIDEBAR_VISIBLE] (state, visible) {
      state.sidebarVisible = visible
    },
    [UI.LANGUAGE] (state, language) {
      I18n.locale = language
      state.language = language
    },
    [UI.PROGRESS_START] (state) {
      if (state.progressStatus !== state) {
        state.progressStatus = 'start'
      }
    },
    [UI.PROGRESS_STOP] (state) {
      if (state.progressStatus !== state) {
        state.progressStatus = 'stop'
      }
    },
    [UI.PROGRESS_FAIL] (state) {
      if (state.progressStatus !== state) {
        state.progressStatus = 'fail'
      }
    }
  }
}
