import md5 from 'md5/md5'
import BaseModel from '@/models/base'
import Email from '@/models/email'

export default class User extends BaseModel {
  defaultValues () {
    return {
      pk: null,
      emails: [],
      firstName: null,
      lastName: null,
      isActive: null,
      isSuperuser: null,
      username: null
    }
  }

  cleanEmails (value) {
    this.emails.splice(0, this.emails.length)
    value.forEach(e => { this.emails.push(new Email(e)) })
  }

  cleanLastLogin (value) {
    if (value) {
      this.lastLogin = new Date(value)
    } else {
      this.lastLogin = null
    }
  }

  cleanDateJoined (value) {
    if (value) {
      this.dateJoined = new Date(value)
    } else {
      this.dateJoined = null
    }
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
    return this.username
  }

  get displayName () {
    if (this.firstName) return this.firstName
    return this.username
  }

  get avatar () {
    return `https://www.gravatar.com/avatar/${md5(this.email || '')}?s=100&d=retro`
  }
}
