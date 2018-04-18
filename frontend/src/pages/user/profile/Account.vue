<template>
  <v-layout row wrap>
    <v-flex xs12 sm10 offset-sm1 md6 offset-md3>
      <v-card class="mb-3" style="margin-top: -40px">
        <v-card-text class="py-0">
          <v-list three-line class="py-2">
            <v-list-tile class="list-in-card">
              <v-list-tile-sub-title>
                {{ $t('label.joined-at', {date: dateJoined}) }}
              </v-list-tile-sub-title>
            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>

      <v-subheader class="pl-0" style="height: 30px;">{{ $t('label.personal-info') }}</v-subheader>
      <v-card>
        <v-card-text>
          <v-form @submit.prevent="submit" ref="form">
            <!-- TODO: Add propper verification for username -->
            <v-text-field :label="$t('label.username')" name="username" ref="username" type="text" tabindex="1" required
                          v-validate="'required'"
                          :data-vv-as="$t('label.username')"
                          :error-messages="errors.collect('username')"
                          v-model="username">
            </v-text-field>
            <v-text-field :label="$t('label.first-name')" name="firstname" ref="firstname" type="text" tabindex="2" required
                          v-validate="'required'"
                          :data-vv-as="$t('label.first-name')"
                          :error-messages="errors.collect('firstname')"
                          v-model="firstName">
            </v-text-field>
            <v-text-field :label="$t('label.last-name')" name="lastname" ref="lastname" type="text" tabindex="2" required
                          v-validate=""
                          :data-vv-as="$t('label.last-name')"
                          :error-messages="errors.collect('lastname')"
                          v-model="lastName">
            </v-text-field>
            <v-btn block color="blue" class="white--text" :disabled="errors.any()" type="submit" :loading="working" tabindex="4">{{ $t('label.save') }}</v-btn>
          </v-form>
        </v-card-text>
      </v-card>

      <error-bottom-sheet :non-field-errors="nonFieldErrors" @clear-errors="clearNonFieldErrors()"/>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'UserProfileAccount',

  mixins: [FormMixin],

  data () {
    return {
      username: '',
      firstName: '',
      lastName: '',
      working: false
    }
  },

  computed: {
    ...mapGetters(['currentUser']),

    dateJoined () {
      return this.currentUser.dateJoined.toLocaleString(
        navigator.language,
        { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
      )
    }
  },

  methods: {
    ...mapActions(['fetchUserData']),

    loadData () {
      this.username = this.currentUser.username
      this.firstName = this.currentUser.firstName
      this.lastName = this.currentUser.lastName
    },

    submit () {
      this.$validator.validateAll().then(valid => {
        if (valid) {
          const data = {
            username: this.username,
            first_name: this.firstName,
            last_name: this.lastName
          }
          this.working = true

          this.$http.put('/api/auth/user/', data)
            .then(data => data.json())
            .then(obj => this.fetchUserData())
            .then(user => {
              this.$toasts.open({ text: this.$t('message.profile-updated') })
              this.loadData()
            })
            .catch(err => { this.processErrors(err) })
            .finally(() => { this.working = false })
        }
      })
    }
  },

  mounted () {
    this.loadData()
  }
}
</script>
