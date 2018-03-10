import Vue from 'vue'
import { USER, UI } from '@/store/mutation-types'
import User from '@/models/user'

export default {
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
    commit(UI.PROGRESS_START)
    return new Promise((resolve, reject) => {
      Vue.http.post('/api/auth/login/', credentials)
        .then(data => data.json())
        .then(data => dispatch('fetchUserData'))
        .then(user => {
          resolve(user)
        })
        .catch(err => {
          reject(err)
          commit(UI.PROGRESS_FAIL)
        })
    })
  },

  fetchUserData ({ commit }) {
    return new Promise((resolve, reject) => {
      Vue.http.get('/api/auth/user/')
        .then(data => data.json())
        .then(data => {
          let user = User.fromJson(data)
          commit(USER.FETCH_DATA, user)
          resolve(user)
        })
        .catch(err => {
          reject(err)
        })
    })
  },

  logout ({ commit }) {
    commit(UI.PROGRESS_START)
    return new Promise((resolve, reject) => {
      Vue.http.post('/api/auth/logout/')
        .then(data => data.json())
        .then(data => {
          commit(USER.LOGOUT)
          resolve(data)
        })
        .catch(err => {
          reject(err)
          commit(UI.PROGRESS_FAIL)
        })
    })
  }
}
