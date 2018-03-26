<template>
  <v-list-tile class="list-in-card-no-padding">
    <v-list-tile-content>
      <v-list-tile-title>
        Origin {{ block.ip_address }} locked out {{ block.attempt_time | moment('from') }}.
      </v-list-tile-title>
      <v-list-tile-sub-title>
        <span v-if="unlocked">
          This origin was unlocked!
        </span>
        <span v-else>
          Will be unlocked in {{ countdown }}
        </span>
      </v-list-tile-sub-title>
    </v-list-tile-content>
    <v-list-tile-action>
      <v-btn flat icon color="grey" @click=""><v-icon>info</v-icon></v-btn>
    </v-list-tile-action>
  </v-list-tile>
</template>

<script>
export default {
  name: 'BlockedOriginItem',

  props: {
    block: {
      type: Object
    }
  },

  data () {
    return {
      unlocked: false,
      countdown: '...',
      countdownInterval: null
    }
  },

  methods: {
    updateCountdown () {
      // TODO: Fix now with UTC
      if (this.unlocked) {
        return
      }

      let now = new Date()
      let start = this.$moment(now)
      let end = this.$moment(this.block.block_end)

      if ((this.block.block_end - now) <= 0) {
        this.unlocked = true
      } else {
        let hours = end.diff(start, 'hours')
        let minutes = end.diff(start, 'minutes') - (hours * 60)
        let seconds = end.diff(start, 'seconds') - (minutes * 60) - (hours * 60 * 60)

        if (hours) {
          this.countdown = `${hours} hours, ${minutes} minutes and ${seconds} seconds`
        } else if (minutes) {
          this.countdown = `${minutes} minutes and ${seconds} seconds`
        } else {
          this.countdown = `${seconds} seconds`
        }
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
