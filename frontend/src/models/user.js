import md5 from 'md5/md5'
import BaseModel from '@/models/base'

export default class User extends BaseModel {
  constructor (data = {}) {
    data = Object.assign({
      pk: null,
      email: null,
      firstName: null,
      lastName: null,
      isActive: null,
      isSuperuser: null,
      username: null
    }, data)

    super(data)
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
