import Vue from 'vue'

import actions from './actions'
import User from '@/models/User'
import { AUTH } from '@/store/mutation-types'

export default {
  state: {
    sessions: {},
    user: new User()
  },

  getters: {
    currentUser (state) { return state.user },
    getSessions (state) {
      return Object.values(state.sessions).sort((a, b) => a.updatedAt > b.updatedAt)
    }
  },

  mutations: {
    [AUTH.SESSIONS] (state, sessions) {
      state.sessions = {}
      for (let session of sessions) {
        state.sessions[session.pk] = session
      }
    },

    [AUTH.REMOVE_SESSION] (state, session) {
      Vue.delete(state.sessions, session.pk)
    },

    [AUTH.FETCH_DATA] (state, user) {
      state.user = user
    },

    [AUTH.LOGOUT] (state, user) {
      state.user = new User()
      Vue.cookies.remove('csrftoken')
    }
  },

  actions: actions
}
