<template>
  <user-list />
</template>

<script>
import UserList from '@/components/manage/UserList'

export default {
  name: 'ManageUsersPage',

  route: {
    name: 'manage-users',
    layout: 'Dashboard',
    middlewares: ['PrivateOnly'],
    breadcrumbs: [
      {title: 'Management'},
      {title: 'Users'}
    ]
  },

  components: { UserList },

  data () {
    return {
    }
  }
}
</script>
