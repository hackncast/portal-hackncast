export const state = () => ({
  darkTheme: (localStorage.getItem('UI_DarkTheme') === 'true')
})

export const getters = {
}

export const mutations = {
  DARK_THEME (state, value) {
    state.darkTheme = value
    localStorage.setItem('UI_DarkTheme', value)
  }
}

export const actions = {
}
