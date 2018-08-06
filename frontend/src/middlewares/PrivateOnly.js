import store from '@/store'

export default function (to, from, next) {
  if (store.state.auth.user.isAuthenticated) {
    return next()
  }

  store.dispatch('auth/fetchUser')
    .then(user => next())
    .catch(() => next({name: 'auth-login', query: {next: to.path}}))
}
