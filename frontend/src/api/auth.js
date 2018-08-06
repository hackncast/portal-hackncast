export default (axios) => ({
  fetchUser () {
    return axios.get('/auth/user/')
  }
})
