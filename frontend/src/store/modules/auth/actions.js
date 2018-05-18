import { AUTH } from '@/store/mutation-types'
import UserSession from '@/models/UserSession'

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
  }
}
