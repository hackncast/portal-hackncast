<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-title class="title">Primary Email</v-card-title>
        <v-card-text class="grey--text pt-0">
          {{ primaryEmailAddress }}
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-title class="title">Registered Emails</v-card-title>
        <v-card-text class="pt-0">
          <v-list>
            <v-list-tile v-for="email in emails" :key="email.pk">
              <v-list-tile-content>
                <v-list-tile-title>{{ email.email }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ email.verified ? 'Verified' : 'Not verified yet!'}}</v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon ripple>
                  <v-icon color="grey lighten-1">more_vert</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>

    <v-speed-dial fixed bottom right open-on-hover
                  direction="top" transition="slide-y-reverse-transition"
                  v-model="fab">
      <v-btn dark fab hover slot="activator"
             color="blue darken-2" v-model="fab">
        <v-icon>settings</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-tooltip left>
        <v-btn fab dark small color="green" slot="activator">
          <v-icon>add</v-icon>
        </v-btn>
        <span>Add new email</span>
      </v-tooltip>
      <v-tooltip left>
        <v-btn fab dark small color="indigo" slot="activator">
          <v-icon>edit</v-icon>
        </v-btn>
        <span>Change default email</span>
      </v-tooltip>
    </v-speed-dial>
    </v-flex>
  </v-layout>
</template>

<script>
// import Vue from 'vue'
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'UserProfileEmails',

  mixins: [FormMixin],

  data () {
    return {
      fab: false,
      emails: [],
      primaryEmail: null
    }
  },

  computed: {
    primaryEmailAddress () {
      return this.primaryEmail !== null ? this.primaryEmail.email : ''
    }
  },

  methods: {
    fetchEmails () {
      this.$progress.start()
      this.emails.splice(0, this.emails.length)
      this.$http.get('/api/user/email/')
        .then(data => data.json())
        .then(emails => {
          for (let email of emails) {
            this.emails.push(email)
            if (email.primary) {
              this.primaryEmail = email
            }
          }
        })
        .catch(() => {
          this.$progress.fail()
        })
        .finally(() => this.$progress.stop())
    }
  },

  mounted () {
    this.fetchEmails()
  }
}
</script>
