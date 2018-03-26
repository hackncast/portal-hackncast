<template>
  <v-card class="mb-3">
    <v-card-text class="py-0">
      <v-list>
        <v-list-tile class="list-in-card">
          <v-list-tile-content>
            <v-list-tile-sub-title>
              We've found <span class="red--text">{{ failCount }} failed login attempt</span> from {{ ipsCount }} different origins in the last 7 days.
            </v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn flat icon color="grey" @click=""><v-icon>info</v-icon></v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'AccessAttempts',

  props: {
    attempts: {
      type: Array
    }
  },

  computed: {
    failedAttempts () {
      return this.attempts.filter(attempt => attempt.login_valid === false)
    },
    failCount () {
      return this.failedAttempts.length
    },
    ipsCount () {
      return (new Set(this.failedAttempts.map(attempt => attempt.ip_address))).size
    }
  }
}
</script>
