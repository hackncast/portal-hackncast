<template>
  <v-card class="mb-3 px-2">
    <zoom-center-transition group>
      <template v-for="(session, index) in currentSessions">
        <v-divider v-if="index !== 0" :key="index" />
        <user-session-item :session="session" :key="session.pk" @end="endSession(session.pk)" @openDialog="(url) => openMapDialog(url)"/>
      </template>
    </zoom-center-transition>
    <div v-if="currentSessions.length === 0" class="pa-3">
      No active sessions found
    </div>

    <v-dialog v-model="mapDialog" max-width="">
      <v-card>
        <v-card-title class="body-2">Approximated Access Location</v-card-title>
        <v-card-text>
          <div v-cloak>
            <img :src="mapUrl" border="0" style="width: 100%; border-radius: 3px"/>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" flat @click.stop="closeMapDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      mapUrl: null,
      mapDialog: false,
      currentSessions: this.sessions
    }
  },

  methods: {
    endSession (pk) {
      this.$progress.start()
      this.$http.delete(`/api/user/session/${pk}/`)
        .then(() => {
          this.currentSessions = this.currentSessions.filter(session => session.pk !== pk)
          this.$progress.stop()
        })
        .catch(() => {
          this.$progress.fail()
          this.$toasts.open({ text: 'An error ocurred while excluding this session' })
        })
    },
    openMapDialog (url) {
      this.mapDialog = true
      this.mapUrl = url
    },
    closeMapDialog () {
      this.mapDialog = false
      setTimeout(() => {
        this.mapUrl = null
      }, 250)
    }
  }
}
</script>
