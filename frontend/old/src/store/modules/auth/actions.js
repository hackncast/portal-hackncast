import Vue from 'vue'

import { AUTH } from '@/store/mutation-types'
import UserSession from '@/models/UserSession'
import UserService from '@/services/User'

export default {
  fetchUserSessions ({ commit }) {
    UserSession.service.all()
      .then(data => {
        commit(AUTH.SESSIONS, data)
      })
      .catch(err => { throw err })
  },

  removeUserSession ({ commit, state }, session) {
    session.delete()
      .then(data => {
        commit(AUTH.REMOVE_SESSION, session)
      })
      .catch(err => { throw err })
  },

  checkStoredLogin ({ getters, dispatch, commit, state }) {
    return new Promise((resolve, reject) => {
      if (state.user.isAuthenticated) {
        resolve(state.user)
      } else {
        dispatch('fetchUserData')
          .then(res => resolve(res))
          .catch(err => reject(err))
      }
    })
  },

  login ({ dispatch, commit }, credentials) {
    return new Promise((resolve, reject) => {
      Vue.http.post('/api/auth/login/', credentials)
        .then(data => data.json())
        .then(data => dispatch('fetchUserData'))
        .then(user => {
          resolve(user)
        })
        .catch(err => {
          reject(err)
        })
    })
  },

  fetchUserData ({ commit }) {
    return new Promise((resolve, reject) => {
      UserService.getCurrentUser()
        .then(user => {
          commit(AUTH.FETCH_DATA, user)
          resolve(user)
        })
        .catch(err => reject(err))
    })
  },

  logout ({ commit }) {
    return new Promise((resolve, reject) => {
      Vue.http.post('/api/auth/logout/')
        .then(data => data.json())
        .then(data => {
          commit(AUTH.LOGOUT)
          resolve(data)
        })
        .catch(err => {
          reject(err)
        })
    })
  }
}
