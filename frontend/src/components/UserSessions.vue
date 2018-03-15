<template>
  <v-card class="mb-3 px-2">
      <template v-for="(session, index) in sessions">
      <user-session-item :session="session" :key="session.pk" />
      <v-divider v-if="index !== sessions.length" :key="index" />
    </template>
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
  }
}
</script>
