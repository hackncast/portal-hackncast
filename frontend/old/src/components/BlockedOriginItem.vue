<template>
  <v-list-tile class="list-in-card-no-padding py-2">
    <!-- TODO: Localize moment.js -->
    <v-list-tile-content>
      <v-list-tile-title>
        {{ $t('profile.blockedOrigin.title', {address: block.ip_address, ago: $moment(block.attempt_time).from() }) }}
      </v-list-tile-title>
      <v-list-tile-sub-title>
        <span v-if="unlocked">
          {{ $t('profile.blockedOrigin.unlocked') }}
        </span>
        <span v-else>
          {{ $t('profile.blockedOrigin.waiting', { countdown }) }}
        </span>
      </v-list-tile-sub-title>
    </v-list-tile-content>
    <v-list-tile-action>
      <v-btn flat icon color="grey" @click="$emit('unblock', block.ip_address)"><v-icon>no_encryption</v-icon></v-btn>
    </v-list-tile-action>
  </v-list-tile>
</template>

<script>
export default {
  name: 'BlockedOriginItem',

  props: {
    block: Object
  },

  data () {
    return {
      endBlock: this.$moment().add(this.block.ttl, 'seconds'),
      unlocked: false,
      countdown: '...',
      countdownInterval: null
    }
  },

  methods: {
    updateCountdown () {
      let now = this.$moment()

      if (this.unlocked || now.isAfter(this.endBlock)) {
        this.unlocked = true
        clearInterval(this.countdownInterval)
      }

      let hours = this.endBlock.diff(now, 'hours')
      let minutes = this.endBlock.diff(now, 'minutes') - (hours * 60)
      let seconds = this.endBlock.diff(now, 'seconds') - (minutes * 60) - (hours * 60 * 60)

      hours = this.$tc('label.hours', hours, { hours })
      minutes = this.$tc('label.minutes', minutes, { minutes })
      seconds = this.$tc('label.seconds', seconds, { seconds })

      if (hours) {
        this.countdown = `${hours}, ${minutes} ${this.$t('label.and')} ${seconds}...`
      } else if (minutes) {
        this.countdown = `${minutes} ${this.$t('label.and')} ${seconds}...`
      } else {
        this.countdown = seconds + '...'
      }
    }
  },

  mounted () {
    this.countdownInterval = setInterval(this.updateCountdown, 1000)
  },

  destroyed () {
    if (this.countdownInterval) clearInterval(this.countdownInterval)
  }
}
</script>
