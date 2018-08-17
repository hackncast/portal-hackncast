import BaseModel from '@/models/base'

export default class Email extends BaseModel {
  constructor (data = {}) {
    data = Object.assign({
      pk: null,
      email: null,
      verified: null,
      primary: null
    }, data)

    super(data)
  }
}
