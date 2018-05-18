import Vue from 'vue'
import actions from './actions'
import User from '@/models/User'
import { USER } from '@/store/mutation-types'

export default {
  state: {
    user: new User()
  },

  getters: {
    currentUser (state) {
      return state.user
    }
  },

  mutations: {
    [USER.FETCH_DATA] (state, user) {
      state.user = user
    },
    [USER.LOGOUT] (state, user) {
      state.user = new User()
      Vue.cookies.remove('csrftoken')
    }
  },

  actions: actions
}
