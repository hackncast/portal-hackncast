<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-text class="grey--text">
          Last login at {{ lastLogin }}
        </v-card-text>
      </v-card>

      <v-card class="mb-3">
        <v-card-text class="grey--text">
          <template v-if="passwords.length === 0">
            Hey, you still use your first password from {{ dateJoined }}? Consider changing it soon...
          </template>
          <template v-else>
            You have changed your password {{ passwords.length }} time<span v-if="passwords.length > 1">s</span> since {{ lastChanged }}
          </template>
        </v-card-text>
      </v-card>

      <change-password-form :show="showChangePasswordForm" @close="showChangePasswordForm = false" />

    </v-flex>
  </v-layout>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'
import { mapGetters } from 'vuex'
import ChangePasswordForm from '@/components/forms/user/ChangePassword'

export default {
  name: 'UserProfileSecurity',

  components: { ChangePasswordForm },

  mixins: [FormMixin],

  data () {
    return {
      showChangePasswordForm: false,
      passwords: []
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
    fetchPasswords () {
      this.$progress.start()
      this.$http.get('/api/user/password/')
        .then(data => data.json())
        .then(passwords => {
          this.passwords.splice(0, this.passwords.length)
          for (let password of passwords) {
            this.passwords.push(new Date(password.changed_at))
          }
          this.$progress.stop()
        })
        .catch(() => this.$progress.fail())
    }
  },

  mounted () {
    this.fetchPasswords()
  }
}
</script>
