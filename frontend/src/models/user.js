import md5 from 'md5/md5'

export default class User {
  constructor (pk = null, username = null, email = null, firstName = null, lastName = null, isActive = null, isSuperuser = null, verifiedEmail = null, pkEmail = null, dateJoined = null, lastLogin = null) {
    this.pk = pk
    this.username = username
    this.email = email
    this.firstName = firstName
    this.lastName = lastName
    this.isActive = isActive
    this.isSuperuser = isSuperuser
    this.verifiedEmail = verifiedEmail
    this.pkEmail = pkEmail
    this.dateJoined = new Date(dateJoined)
    this.lastLogin = new Date(lastLogin)
  }

  get avatar () {
    return `https://www.gravatar.com/avatar/${md5(this.email || '')}?s=100&d=retro`
  }

  get isAuthenticated () {
    return this.pk !== null
  }

  get displayName () {
    if (this.firstName) {
      return this.firstName
    } else if (this.username) {
      return this.username.charAt(0).toUpperCase() + this.username.slice(1)
    }
    return ''
  }

  get safeEmailAddress () {
    if (this.email) {
      let parts = this.email.split('@')
      return parts[0].slice(0, 3) + parts[0].slice(3, parts[0].length).replace(/./g, '*') + '@' + parts[1]
    } else {
      return ''
    }
  }

  static fromJson (data) {
    return new User(
      data.pk,
      data.username,
      data.email,
      data.first_name,
      data.last_name,
      data.is_active,
      data.is_superuser,
      data.verified_email,
      data.email_pk,
      data.date_joined,
      data.last_login
    )
  }
}
