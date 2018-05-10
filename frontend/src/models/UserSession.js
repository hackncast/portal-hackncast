import moment from 'moment/moment'
import BaseModel from '@/models/Base'
import services from '@/services'

export default class UserSessionModel extends BaseModel {
  static service = services.UserSession

  constructor (data = {
    pk: null,
    expireDate: null,
    userAgent: null,
    updatedAt: null,
    ip: null,
    current: null
  }) {
    if (data.expireDate !== null) data.expireDate = moment(data.expireDate)
    if (data.updatedAt !== null) data.updatedAt = moment(data.updatedAt)

    super(data)
  }
}
