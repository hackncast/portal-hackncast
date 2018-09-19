export default (axios) => ({
  fetchUsers (options = {page: 1, size: 10}) {
    return axios.get('/manage/user/', {params: options})
  },

  updateUser (userData) {
    return axios.patch(`/manage/user/${userData.pk}/`, userData)
  }
})
