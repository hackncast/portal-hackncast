<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-title class="title pb-0 pt-1">
          Primary Email
          <v-spacer></v-spacer>
          <v-btn flat icon color="grey" @click="changePrimaryEmailDialog = true"><v-icon>edit</v-icon></v-btn>
        </v-card-title>
        <v-card-text class="grey--text pt-0">
          {{ primaryEmail }}
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-title class="title pb-0 pt-1">
          Registered Emails
          <v-spacer></v-spacer>
          <v-btn flat icon color="grey" @click="newEmailDialog = true"><v-icon>add</v-icon></v-btn>
        </v-card-title>
        <v-card-text class="pt-0">
          <v-list>
            <v-list-tile v-for="email in emails" :key="email.pk">
              <v-list-tile-content>
                <v-list-tile-title>{{ email.email }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ email.verified ? 'Verified' : 'Not verified yet!'}}</v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-menu bottom left v-if="!email.verified || !email.primary">
                  <v-btn icon ripple slot="activator"><v-icon color="grey lighten-1">more_vert</v-icon></v-btn>
                  <v-list>
                    <v-list-tile @click="resendVerification(email.pk)" :disabled="email.verified">
                      <v-list-tile-title>Resend Verification</v-list-tile-title>
                    </v-list-tile>
                    <v-list-tile @click="excludeEmail(email.pk)"  :disabled="email.primary">
                      <v-list-tile-title>Exclude</v-list-tile-title>
                    </v-list-tile>
                  </v-list>
                </v-menu>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>

      <user-email-form :show="newEmailDialog" @close="newEmailDialog = false" @success="fetchEmails" />

      <v-dialog v-model="changePrimaryEmailDialog" max-width="290">
        <v-card>
          <v-card-title class="headline pb-0">Change Primary Email Address</v-card-title>
          <v-card-text class="pt-0">
          <v-select :items="elegibleForPrimary" v-model="newPrimaryEmail" label="Select" single-line></v-select>
          <strong class="blue--text">Note:</strong> An email MUST be verified before being set as primary.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" flat="flat" @click.native="changePrimaryEmailDialog = false; newPrimaryEmail = primaryEmail">Cancel</v-btn>
            <v-btn color="green darken-1" flat="flat" @click="setAsPrimaryEmail" :loading="working" :disabled="newPrimaryEmail === primaryEmail" tabindex="1">Set as Primary</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-flex>
  </v-layout>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'
import UserEmailForm from '@/components/forms/user/Email'

export default {
  name: 'UserProfileEmails',

  mixins: [FormMixin],

  components: { UserEmailForm },

  data () {
    return {
      working: false,
      newEmailDialog: false,
      changePrimaryEmailDialog: false,
      emails: [],
      primaryEmail: '',
      newPrimaryEmail: null
    }
  },

  computed: {
    elegibleForPrimary () {
      // return this.emails.filter(email => email.verified)
      return this.emails.map(email => email.email)
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
              this.primaryEmail = email.email
            }
          }
          this.newPrimaryEmail = this.primaryEmail
          this.$progress.stop()
        })
        .catch(() => {
          this.$progress.fail()
        })
    },

    resendVerification (pk) {
      this.$progress.start()
      this.$http.post(`/api/user/email/${pk}/send_confirmation/`)
        .then(data => data.json())
        .then(data => {
          this.$progress.stop()
        })
        .catch(() => {
          this.$progress.fail()
        })
    },

    excludeEmail (pk) {
      this.$progress.start()
      this.$http.delete(`/api/user/email/${pk}/`)
        .then(data => data.json())
        .then(data => {
          this.$progress.stop()
          this.fetchEmails()
        })
        .catch(() => {
          this.$progress.fail()
        })
    },

    setAsPrimaryEmail () {
      const newPrimary = this.emails.find(email => email.email === this.newPrimaryEmail)
      this.$progress.start()
      this.$http.put(`/api/user/email/${newPrimary.pk}/`)
        .then(data => {
          this.$progress.stop()
          this.fetchEmails()
          this.changePrimaryEmailDialog = false
        })
        .catch(() => {
          this.$progress.fail()
          this.newPrimaryEmail = this.primaryEmail
        }).finally(() => {
          this.working = false
        })
    }
  },

  mounted () {
    this.fetchEmails()
  }
}
</script>
