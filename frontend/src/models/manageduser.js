import User from '@/models/user'

export default class ManagedUser extends User {
  defaultValues () {
    return {
      pk: null,
      emails: [],
      firstName: null,
      lastName: null,
      username: null,
      dateJoined: null,
      lastLogin: null,
      groups: [],
      isStaff: null
    }
  }
}
