
import Vue from 'vue'
import ManagedUser from '@/models/manageduser'

export const state = () => ({
  usersPage: {
    page: null,
    numPages: null,
    count: null,
    next: null,
    previous: null,
    results: []
  }
})

export const getters = {
  users: (state) => { return state.usersPage.results }
}

export const mutations = {
  SET_USERS: function (state, data) {
    // update results
    state.usersPage.results.splice(0, state.usersPage.results.length)
    data.results.map(raw => {
      state.usersPage.results.push(ManagedUser.fromJson(raw))
    })
    // update pagination data
    state.usersPage.page = data.page
    state.usersPage.numPages = data.numPages
    state.usersPage.count = data.count
    state.usersPage.next = data.next
    state.usersPage.previous = data.previous
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
  }
}
