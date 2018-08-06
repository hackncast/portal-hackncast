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
}
