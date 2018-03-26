<template>
  <v-card class="mb-3">
    <v-card-text class="py-0">
      <v-list>
        <template v-for="block in blocks">
          <blocked-origin-item :block="block" :key="block.ip_address" />
        </template>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import BlockedOriginItem from '@/components/BlockedOriginItem'

export default {
  name: 'BlockedOrigins',

  components: { BlockedOriginItem },

  props: {
    blocks: {
      type: Array
    }
  }
}
</script>
