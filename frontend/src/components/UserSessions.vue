<template>
  <v-card class="mb-3 px-2">
    <template v-for="(session, index) in currentSessions">
      <user-session-item :session="session" :key="session.pk" @end="endSession(session.pk)"/>
      <v-divider v-if="index !== currentSessions.length" :key="index" />
    </template>
    <div v-if="currentSessions.length === 0" class="pa-3">
      No active sessions found
    </div>
  </v-card>
</template>

<script>
import UserSessionItem from '@/components/UserSessionItem'

export default {
  name: 'UserSessions',

  components: { UserSessionItem },

  props: {
    sessions: {
      type: Array
    }
  },

  data () {
    return {
      currentSessions: this.sessions
    }
  },

  methods: {
    endSession (pk) {
      this.currentSessions = this.currentSessions.filter(session => session.pk !== pk)
    }
  }
}
</script>
