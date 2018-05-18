<template>
  <v-card class="mb-3 px-2">
    <zoom-center-transition group>
      <template v-for="(session, index) in getSessions">
        <v-divider v-if="index !== 0" :key="index" />
        <user-session-item :session="session" :key="session.pk" @end="endSession(session)" @openDialog="(url) => openMapDialog(url)"/>
      </template>
    </zoom-center-transition>
    <div v-if="getSessions.length === 0" class="pa-3">
      {{ $t('profile.session.no-active-sessions') }}
    </div>

    <v-dialog v-model="mapDialog" max-width="">
      <v-card>
        <v-card-title class="body-2">{{ $t('profile.session.approximate-location') }}</v-card-title>
        <v-card-text>
          <div v-cloak>
            <img :src="mapUrl" border="0" style="width: 100%; border-radius: 3px"/>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
            <v-btn color="primary" flat @click.stop="closeMapDialog">{{ $t('label.close') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'
import UserSessionItem from '@/components/UserSessionItem'

export default {
  name: 'UserSessions',

  components: { UserSessionItem },

  data () {
    return {
      mapUrl: null,
      mapDialog: false
    }
  },

  computed: {
    ...mapState({
      sessions: state => state.Auth.sessions
    }),
    ...mapGetters(['getSessions'])
  },

  methods: {
    ...mapActions([
      'fetchUserSessions', 'removeUserSession'
    ]),

    endSession (session) {
      this.removeUserSession(session)
        .then(data => this.$progress.stop())
        .catch(err => {
          this.$progress.fail()
          this.$toasts.open({ text: 'An error ocurred while excluding this session' })
          throw err
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
  },

  created () {
    this.fetchUserSessions()
  }
}
</script>
