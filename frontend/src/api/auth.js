export default (axios) => ({
  fetchUser () {
    return axios.get('/auth/user/')
  },

  registration (data) {
    return axios.post('/auth/registration/', data)
  },

  login (data) {
    return axios.post('/auth/login/', data)
  },

  resetPassword (data) {
    return axios.post('/auth/password/reset/', data)
  }
})
