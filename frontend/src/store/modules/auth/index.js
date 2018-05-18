import Vue from 'vue'
import actions from './actions'
import { AUTH } from '@/store/mutation-types'

export default {
  state: {
    sessions: {}
  },

  getters: {
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
    }
  },

  actions: actions
}
