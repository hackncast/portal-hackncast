<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-text class="grey--text text--darken-2">
          Last login at {{ lastLogin }}
        </v-card-text>
      </v-card>

      <h2 class="subheading mb-1 grey--text text--darken-3">Password</h2>
      <v-card class="mb-3">
        <v-card-text class="grey--text text--darken-4">
          <template v-if="passwords.length === 0">
            Hey, you still use your first password from {{ dateJoined }}? Please, consider changing it soon...
          </template>
          <template v-else>
            You have changed your password {{ passwords.length }} time<span v-if="passwords.length > 1">s</span>. Last time was {{ lastChanged }}.
          </template>
        </v-card-text>
        <v-card-actions>
          <v-btn flat block color="blue" @click="showChangePasswordForm = true">Change Password</v-btn>
        </v-card-actions>
      </v-card>

      <h2 class="subheading mb-1 grey--text text--darken-3">Sessions</h2>
      <user-sessions :sessions="sessions" />

      <change-password-form :show="showChangePasswordForm" @close="showChangePasswordForm = false" />

    </v-flex>
  </v-layout>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'
import { mapGetters } from 'vuex'
import ChangePasswordForm from '@/components/forms/user/ChangePassword'
import UserSessions from '@/components/UserSessions'

export default {
  name: 'UserProfileSecurity',

  components: { ChangePasswordForm, UserSessions },

  mixins: [FormMixin],

  data () {
    return {
      showChangePasswordForm: false,
      passwords: [],
      sessions: []
    }
  },

  computed: {
    ...mapGetters(['currentUser']),

    lastChanged () {
      return this.passwords[0].toLocaleString(
        navigator.language,
        { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
      )
    },

    lastLogin () {
      return this.currentUser.lastLogin.toLocaleString(
        navigator.language,
        { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
      )
    },

    dateJoined () {
      return this.currentUser.dateJoined.toLocaleString(
        navigator.language,
        { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
      )
    }
  },

  methods: {
    fetchData () {
      this.$progress.start()
      this.$http.get('/api/user/password/')
        .then(data => data.json())
        .then(passwords => {
          this.passwords.splice(0, this.passwords.length)
          for (let password of passwords) {
            this.passwords.push(new Date(password.changed_at))
          }
          return this.$http.get('/api/user/session/')
        })
        .then(data => data.json())
        .then(sessions => {
          this.sessions.splice(0, this.sessions.length)
          for (let session of sessions) {
            this.sessions.push(session)
          }
          this.$progress.stop()
        })
        .catch(() => this.$progress.fail())
    }
  },

  mounted () {
    this.fetchData()
  }
}
</script>
