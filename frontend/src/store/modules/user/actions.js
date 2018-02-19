import Vue from 'vue'
import { USER } from '@/store/mutation-types'
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

  login ({ dispatch }, credentials) {
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
  }
}
