export default class User {
  constructor (pk = null, username = null, email = null) {
    this.pk = pk
    this.username = username
    this.email = email
  }

  get isAuthenticated () {
    return this.pk !== null
  }

  static fromJson (data) {
    return new User(
      data.pk,
      data.username,
      data.email
    )
  }
}
