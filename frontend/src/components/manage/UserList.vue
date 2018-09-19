<template>
  <paginated-card-list
    action="manage/fetchUsers"
    :state="page"
    size="xs12 sm6 md4 lg3"
    :sorting="sortingOptions"
    >
    <user-list-item slot-scope="props" :user="props.item" />
  </paginated-card-list>
</template>

<script>
import { mapState } from 'vuex'
import PaginatedCardList from '@/components/PaginatedCardList'
import UserListItem from '@/components/manage/UserListItem'

export default {
  name: 'ManageUserList',

  components: { PaginatedCardList, UserListItem },

  data () {
    return {
      sortingOptions: [
        {value: 'full_name', text: 'Name'},
        {value: 'email', text: 'E-mail'},
        {value: 'last_login', text: 'Last Login'},
        {value: 'date_joined', text: 'Date Joined'}
      ]
    }
  },

  computed: {
    ...mapState({
      page: (state) => state.manage.usersPage
    }),

    cardNavClass () {
      return this.$store.state.ui.darkTheme ? 'card--nav--dark' : 'card--nav--light'
    }
  },

  watch: {
    sorting (val) {
      let query = Object.assign({}, this.$route.query)
      query.sort = val.value
      this.$router.push({ name: this.$route.name, query: query })
      console.log('user list push')
    }
  }
}
</script>

<style lang="sass">
.card--nav--dark
  background-color: rgba(0, 0, 0, .3) !important

.card--nav--light
  background-color: rgba(255, 255, 255, .3) !important
</style>
