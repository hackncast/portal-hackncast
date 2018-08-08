import Vue from 'vue'
import User from '@/models/user'

export const state = () => ({
  user: User.fromJson({})
})

export const getters = {
  currentUser: (state) => { return state.user }
}

export const mutations = {
  SET_USER: function (state, data) {
    state.user = User.fromJson(data)
  }
}

export const actions = {
  fetchUser ({commit, state}) {
    return Vue.api.auth.fetchUser()
      .then(response => {
        commit('SET_USER', response.data)
        return state.user
      })
      .catch(err => { throw err })
  },

  login ({commit, state}, data) {
    return Vue.api.auth.login(data)
      .then(response => {
        return response
      })
      .catch(err => { throw err })
  }
}
