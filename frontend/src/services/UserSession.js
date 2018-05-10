import BaseService from './Base'

export default class UserSessionService extends BaseService {
  static __endpoint = {
    context: 'user',
    name: 'session'
  }
}
