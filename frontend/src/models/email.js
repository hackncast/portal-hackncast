import BaseModel from '@/models/base'

export default class Email extends BaseModel {
  defaultValues () {
    return {
      pk: null,
      email: null,
      verified: null,
      primary: null
    }
  }
}
