<template>
  <v-card class="elevation-0">
    <v-container fluid grid-list-lg class="px-0 py-2">
      <transition name="fade" mode="out-in">
        <v-layout row wrap v-if="ready" key="map">
          <v-flex xs4 class="pb-0">
            <img @click="onMapClick" :src="mapUrl" :alt="$t('messages.approximate-location')" border="0" style="width: 100%; border-radius: 3px" :class=" bogon ? 'not-clickable' : 'clickable'"/>
          </v-flex>
          <v-flex xs8 class="pb-0">
            <div class="body-2">{{ header }}</div>
            <div class="caption grey--text">{{ session.ip }}</div>
            <div class="caption">{{ $t('labels.expires') }} {{ session.expire_date | moment('from') }}</div>
            <div class="caption">{{ $t('labels.last-activity') }}, {{ session.updated_at | moment('from') }}</div>
            <div class="caption red--text" v-if="session.current === true">{{ $t('labels.current-session') }}</div>
            <div class="hidden-xs-only">
              <div class="caption grey--text"><strong>{{ $t('labels.ip-address') }}:</strong> {{ session.ip }}</div>
              <div class="caption grey--text"><strong>User Agent: </strong>{{ session.user_agent }}</div>
            </div>
          </v-flex>
          <v-flex xs12 class="hidden-sm-and-up">
            <div class="caption grey--text"><strong>User Agent: </strong>{{ session.user_agent }}</div>
          </v-flex>
        </v-layout>
        <v-layout row v-else key="loading">
          <v-flex xs12 style="min-height: 6em">
            <v-progress-circular indeterminate color="blue" style="margin-left: auto; margin-right: auto; display: block; margin-top: 1.5em;" />
          </v-flex>
        </v-layout>
      </transition>
    </v-container>
    <transition name="fade" mode="out-in">
      <v-card-actions class="px-0 pt-0" v-if="ready">
        <v-btn block flat color="red" class="mx-0" :disabled="session.current === true" @click="$emit('end')">{{ $t('labels.end-session') }}</v-btn>
      </v-card-actions>
    </transition>
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
    mapSize () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return '150x150'
        case 'sm': return '200x200'
        case 'md': return '200x200'
        case 'lg': return '300x300'
        case 'xl': return '300x300'
      }
    },
    bigMapSize () {
      return `${innerWidth}x${innerWidth}`
    },
    mapUrl () {
      if (this.bogon) {
        return `https://maps.googleapis.com/maps/api/staticmap?center=0,0&zoom=0&size=${this.mapSize}&maptype=roadmap&key=${this.api}`
      } else {
        return `https://maps.googleapis.com/maps/api/staticmap?center=${this.loc}&zoom=13&size=${this.mapSize}&maptype=roadmap&markers=color:blue|label:S|${this.loc}&key=${this.api}`
      }
    },
    bigMapUrl () {
      if (this.bogon) {
        return `https://maps.googleapis.com/maps/api/staticmap?center=0,0&zoom=0&size=${this.bigMapSize}&maptype=roadmap&key=${this.api}`
      } else {
        return `https://maps.googleapis.com/maps/api/staticmap?center=${this.loc}&zoom=15&size=${this.bigMapSize}&maptype=roadmap&markers=color:blue|label:S|${this.loc}&key=${this.api}`
      }
    },
    header () {
      if (this.bogon) {
        return this.$t('messages.no-location')
      } else {
        return `${this.city}, ${this.region} (${this.country})`
      }
    }
  },

  methods: {
    onMapClick () {
      if (!this.bogon) this.$emit('openDialog', this.bigMapUrl)
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
      .finally(() => { this.ready = true })
  }
}
</script>

<style lang="sass">
img.clickable
  cursor: pointer
  opacity: 1
  transition: opacity .5s ease

  &:hover
    background: blue
    opacity: .5
</style>
