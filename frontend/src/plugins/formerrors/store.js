export default {
  namespaced: true,

  state: {
    all: []
  },

  mutations: {
    SET (state, errors) { errors.forEach(err => state.all.push(err)) },
    CLEAR (state) { state.all.empty() }
  },

  actions: {
    clear ({commit}) { commit('CLEAR') },

    show ({commit}, errors) {
      commit('CLEAR')
      if (errors) { commit('SET', errors) }
    }
  }
}
