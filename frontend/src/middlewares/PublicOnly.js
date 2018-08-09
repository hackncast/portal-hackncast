import store from '@/store'

export default function (to, from, next) {
  if (store.state.auth.user.isAuthenticated) {
    return next({name: 'home'})
  }

  store.dispatch('auth/fetchUser')
    .then(user => next({name: 'home'}))
    .catch(() => next())
}
