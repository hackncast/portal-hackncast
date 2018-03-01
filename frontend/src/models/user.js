import md5 from 'md5/md5'

export default class User {
  constructor (pk = null, username = null, email = null) {
    this.pk = pk
    this.username = username
    this.email = email
    this.avatar = `https://www.gravatar.com/avatar/${md5(123)}?s=100&d=retro`
  }

  get isAuthenticated () {
    return this.pk !== null
  }

  get displayName () {
    if (this.username) {
      return this.username.charAt(0).toUpperCase() + this.username.slice(1)
    }
    return ''
  }

  static fromJson (data) {
    return new User(
      data.pk,
      data.username,
      data.email
    )
  }
}
