<template>
  <v-card class="mb-3">
    <v-card-text class="py-1">
      <v-list three-line>
        <v-list-tile class="list-in-card">
          <v-list-tile-content>
            <i18n path="profile.attempts.found" tag="v-list-tile-sub-title">
              <span place="failed" class="red--text">{{ $tc('profile.attempts.failed', failCount, { failCount }) }}</span>
              <span place="origin">{{ $tc('profile.attempts.origin', ipsCount, { ipsCount }) }}</span>
            </i18n>
          </v-list-tile-content>
          <v-list-tile-action style="min-width: 30px">
            <v-btn flat icon color="grey" @click="dialogVisible = true"><v-icon>info</v-icon></v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card-text>

    <access-attempts-dialog :attempts="attempts" :visible='dialogVisible' @close="dialogVisible = false" />
  </v-card>
</template>

<script>
import AccessAttemptsDialog from '@/components/dialog/AccessAttempts'

export default {
  name: 'AccessAttempts',

  components: { AccessAttemptsDialog },

  props: {
    attempts: {
      type: Array
    }
  },

  data () {
    return {
      dialogVisible: false
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
