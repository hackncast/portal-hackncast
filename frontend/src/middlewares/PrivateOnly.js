import store from '@/store'

export default function (to, from, next) {
  console.log('to', to)
  if (store.state.auth.user.isAuthenticated) {
    console.log('Is authed')
    return next()
  }
  console.log('Is not authed')
  next({name: 'auth-login', query: {next: to.path}})
}
