import md5 from 'md5/md5'
import BaseModel from '@/models/base'
import Email from '@/models/email'

export default class User extends BaseModel {
  constructor (data = {}) {
    data = Object.assign({
      pk: null,
      emails: [],
      firstName: null,
      lastName: null,
      isActive: null,
      isSuperuser: null,
      username: null
    }, data)

    data.emails = data.emails.map(e => Email.fromJson(e))
    super(data)
  }

  get primaryEmail () {
    return this.email.find(email => email.primary === true)
  }

  get isAuthenticated () {
    return this.pk !== null
  }

  get fullName () {
    if (this.firstName && this.lastName) return this.firstName + ' ' + this.lastName
    if (this.firstName) return this.firstName
    return 'Usuário Sem Nome'
  }

  get displayName () {
    if (this.firstName) return this.firstName
    return this.username
  }

  get avatar () {
    return `https://www.gravatar.com/avatar/${md5(this.email || '')}?s=100&d=retro`
  }
}
