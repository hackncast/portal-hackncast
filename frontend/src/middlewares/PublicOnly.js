import store from '@/store'

export default function (to, from, next) {
  // TODO: Redirect from it came from
  if (store.state.auth.user.isAuthenticated) {
    return next({name: 'home'})
  }
  next()
}
