<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-text class="grey--text text--darken-1">
          Last login at {{ lastLogin }}
        </v-card-text>
      </v-card>

      <v-subheader class="pl-0" style="height: 30px;">Passwords</v-subheader>
      <v-card class="mb-3">
        <v-card-text class="pb-0">
          <v-list-tile-content>
            {{ $tc('profile.passwordChange', passwords.length, {dateJoined, lastChanged, count: passwords.length })}}
          </v-list-tile-content>
        </v-card-text>
        <v-card-actions>
          <v-btn flat block color="blue" @click="showChangePasswordForm = true">Change Password</v-btn>
        </v-card-actions>
      </v-card>

      <v-subheader class="pl-0" style="height: 30px;">Access Attempt</v-subheader>
      <access-attempts :attempts="attempts" />

      <v-subheader class="pl-0" style="height: 30px;">Blocked Origins</v-subheader>
      <blocked-origins :blocks="blocks" />

      <v-subheader class="pl-0" style="height: 30px;">Sessions</v-subheader>
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
import AccessAttempts from '@/components/AccessAttempts'
import BlockedOrigins from '@/components/BlockedOrigins'

export default {
  name: 'UserProfileSecurity',

  components: { ChangePasswordForm, UserSessions, AccessAttempts, BlockedOrigins },

  mixins: [FormMixin],

  data () {
    return {
      showChangePasswordForm: false,
      passwords: [],
      sessions: [],
      attempts: [],
      blocks: []
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
          return this.$http.get('/api/user/access/')
        })
        .then(data => data.json())
        .then(attempts => {
          this.attempts.splice(0, this.attempts.length)
          for (let attempt of attempts) {
            this.attempts.push(attempt)
          }
          return this.$http.get('/api/user/access/blocked')
        })
        .then(data => data.json())
        .then(blocks => {
          this.blocks.splice(0, this.blocks.length)
          for (let block of blocks) {
            block.attempt_time = new Date(block.attempt_time)
            block.block_end = new Date(block.block_end)
            this.blocks.push(block)
          }
          this.$progress.stop()
        })
        .catch(() => this.$progress.fail())
    }
  },

  created () {
    this.fetchData()
  }
}
</script>
