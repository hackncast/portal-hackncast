import BaseService from './Base'
import UserModel from '@/models/User'

export default class UserService extends BaseService {
  static getCurrentUser () {
    return new Promise((resolve, reject) => {
      return this.api.core.userDetails.query()
        .then(data => data.json())
        .then(data => resolve(UserModel.fromJson(data)))
        .catch(err => reject(err))
    })
  }
}
