<template>
  <v-card class="mb-3">
    <v-card-text class="py-0">
      <v-list v-if="blocks.length > 0">
        <!-- TODO: Add animation -->
        <template v-for="(block, index) in blocks">
          <v-divider v-if="index !== 0" :key="index" />
          <blocked-origin-item :block="block" :key="block.ip_address" @unblock="onUnblock" />
        </template>
      </v-list>
      <v-list v-else three-line class="py-3">
        <v-list-tile class="list-in-card">
          <v-list-tile-sub-title>
            {{ $t('message.no-blocked-origin') }}
          </v-list-tile-sub-title>
        </v-list-tile>
      </v-list>
    </v-card-text>

    <confirm-dialog :visible="confirmDialog" :dialog-key="unblockAddress" @negative="confirmDialog = false" @positive="doUnblock">
      <p style="text-align: justify">{{ $t('dialog.unblock-address.text') }}</p>
      <ul style="margin-left: 2em; margin-bottom: 1.5em">
        <li><strong>{{ unblockAddress }}</strong></li>
      </ul>
      <p style="text-align: justify">{{ $t('dialog.unblock-address.alert') }}</p>
    </confirm-dialog>
  </v-card>
</template>

<script>
import ConfirmDialog from '@/components/dialog/Confirm'
import BlockedOriginItem from '@/components/BlockedOriginItem'

export default {
  name: 'BlockedOrigins',

  components: { BlockedOriginItem, ConfirmDialog },

  data () {
    return {
      blocks: [],
      confirmDialog: false,
      unblockAddress: null
    }
  },

  methods: {
    onUnblock (address) {
      this.unblockAddress = address
      this.confirmDialog = true
    },

    doUnblock (address) {
      this.$http.delete(`/api/user/access/blocked/${address}`)
        .then(data => {
          this.blocks.find((block, key) => {
            if (block.ip_address === address) {
              this.blocks.splice(key, 1)
            }
          })
          this.$toasts.open({ text: this.$t('message.unblock-success'), type: 'success' })
        })
        .catch(() => this.$toasts.open({ text: this.$t('message.unblock-error'), type: 'error' }))
        .finally(() => { this.confirmDialog = false })
    }
  },

  created () {
    this.$http.get('/api/user/access/blocked')
      .then(data => data.json())
      .then(blocks => {
        this.blocks.splice(0, this.blocks.length)
        for (let block of blocks) {
          block.attempt_time = new Date(block.attempt_time)
          this.blocks.push(block)
        }
        this.$progress.stop()
      })
      .catch(() => this.$progress.fail())
  }
}
</script>
