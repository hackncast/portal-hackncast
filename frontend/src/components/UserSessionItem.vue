<template>
  <v-card class="elevation-0">
    <v-container fluid grid-list-lg class="px-0 py-2">
      <transition name="fade" mode="out-in">
        <v-layout row v-if="ready" key="map">
          <v-flex xs4>
            <img :src="mapUrl" alt="Approximate location of access" border="0" style="width: 100%"/>
          </v-flex>
          <v-flex xs8>
            <div class="body-2">{{ header }}</div>
            <div class="caption grey--text" v-if="!bogon">{{ session.ip }}</div>
            <div class="caption">{{ ellipsisDescription }}</div>
          </v-flex>
        </v-layout>
        <v-layout row v-else key="loading">
          <v-flex xs12 style="min-height: 6em">
            <v-progress-circular indeterminate color="blue" style="margin-left: auto; margin-right: auto; display: block; margin-top: 1.5em;" />
          </v-flex>
        </v-layout>
      </transition>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name: 'UserSessionItem',

  data () {
    return {
      ready: false,
      api: 'AIzaSyDR7YhWw71qRiDqfZG04aA7bYcLH5kM-Ls',
      bogon: false,
      loc: null,
      org: null,
      city: null,
      region: null,
      country: null,
      hostname: null
    }
  },

  props: {
    session: {
      type: Object
    }
  },

  computed: {
    ellipsisDescription () {
      let max = 100
      if (this.session.user_agent.length > max) {
        return this.session.user_agent.substring(0, max - 3) + '...'
      }
      return this.session.user_agent
    },
    mapUrl () {
      if (this.bogon) {
        return 'http://via.placeholder.com/150x150?text=No+Map'
      } else {
        return `https://maps.googleapis.com/maps/api/staticmap?center=${this.loc}&zoom=14&size=150x150&maptype=roadmap&markers=color:blue|label:S|${this.loc}&key=${this.api}`
      }
    },
    header () {
      if (this.bogon) {
        return this.session.ip
      } else {
        return `${this.city}, ${this.region} (${this.country})`
      }
    }
  },
  mounted () {
    this.$http.get(`http://ipinfo.io/${this.session.ip}`)
      .then(data => data.json())
      .then(data => {
        if (data.bogon) this.bogon = data.bogon
        if (data.org) this.org = data.org
        if (data.city) this.city = data.city
        if (data.region) this.region = data.region
        if (data.country) this.country = data.country
        if (data.loc) this.loc = data.loc
        if (data.hostname) this.hostname = data.hostname
      })
      .catch(err => console.log(err))
      .finally(() => { this.ready = true })
  }
}
</script>
