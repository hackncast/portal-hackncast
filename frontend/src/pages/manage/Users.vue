<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12>
        <v-card>
          <v-card-title>
            Users
            <v-spacer/>
            <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details />
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="page.results"
            :pagination.sync="pagination"
            :total-items="page.count"
            :rows-per-page-items="[5, 10, 25, 50]"
            >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.fullName }}</td>
              <td>{{ props.item.email }}</td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="warning">
              Sorry, I couldn't find any user with "{{ search }}" in it's name or email address
            </v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

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

  data () {
    return {
      loading: false,
      total: 0,
      pagination: {
        rowsPerPage: 10,
        page: 1
      },
      search: '',
      headers: [
        {text: 'Name', align: 'left', value: 'first_name'},
        {text: 'Email', align: 'left', value: 'email'}
      ]
    }
  },

  computed: {
    ...mapState({
      page: (state) => state.manage.usersPage
    })
  },

  methods: {
    fetchUsers () {
      this.loading = true
      this.$store.dispatch('manage/fetchUsers', {
        page: this.pagination.page,
        size: this.pagination.rowsPerPage,
        sort: this.pagination.sortBy,
        descending: this.pagination.descending
      }).finally(() => { this.loading = false })
    }
  },

  watch: {
    pagination: {
      handler () {
        console.log(this.pagination)
        this.fetchUsers()
      },
      deep: true
    }
  }
}
</script>
