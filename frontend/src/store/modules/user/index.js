import actions from './actions'
import User from '@/models/user'
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
    }
  },

  actions: actions
}
