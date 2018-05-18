import { AUTH } from '@/store/mutation-types'
import UserSession from '@/models/UserSession'

export default {
  fetchUserSessions ({ commit }) {
    return new Promise((resolve, reject) => {
      UserSession.service.all()
        .then(data => {
          commit(AUTH.SESSIONS, data)
          resolve(data)
        })
        .catch(err => {
          reject(err)
        })
    })
  },

  removeUserSession ({ commit, state }, session) {
    return new Promise((resolve, reject) => {
      session.delete()
        .then(data => {
          commit(AUTH.REMOVE_SESSION, session)
          resolve(data)
        })
        .catch(err => reject(err))
    })
  }
}
