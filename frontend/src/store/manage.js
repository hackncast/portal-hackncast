
import Vue from 'vue'
import ManagedUser from '@/models/manageduser'
import { paginatedStoreFactory, setStorePageMutation } from '@/utils'

export const state = () => ({
  usersPage: paginatedStoreFactory()
})

export const getters = {
  users: (state) => { return state.usersPage.results }
}

export const mutations = {
  SET_USERS: setStorePageMutation('usersPage', ManagedUser),

  SET_USER: function (state, newData) {
    let user = state.usersPage.results.findByPk(newData.pk)
    user.fromJson(newData)
  }
}

export const actions = {
  fetchUsers ({commit, state}, options) {
    return Vue.api.manage.fetchUsers(options)
      .then(response => {
        commit('SET_USERS', response.data)
        return state.usersPage
      })
      .catch(err => { throw err })
  },

  updateUser ({commit, state}, userData) {
    return Vue.api.manage.updateUser(userData)
      .then(response => {
        commit('SET_USER', response.data)
        return state.usersPage.results.findByPk(userData.pk)
      })
      .catch(err => { throw err })
  }
}
