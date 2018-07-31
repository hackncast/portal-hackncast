<template>
  <v-dialog :value="visible" persistent>
    <v-card>
      <!-- TODO: Translate this... -->
      <v-card-title class="headline">{{ $t('dialog.access-attempts.title') }}</v-card-title>
      <v-card-text class="py-0">
        <v-data-table
          :headers="headers"
          :items="attempts"
          hide-actions
          disable-initial-sort
          item-key="pk"
          >
          <template slot="items" slot-scope="props">
            <tr @click="props.expanded = !props.expanded">
              <td>{{ props.item.ip_address }}</td>
              <td>{{ props.item.ua.os.name }} {{ props.item.ua.os.version }} <span v-if="props.item.ua.device.vendor">({{ props.item.ua.device.vendor}})</span></td>
              <td>{{ props.item.ua.browser.name }} {{ props.item.ua.browser.major }}</td>
              <td>{{ props.item.ua.engine.name }} {{ props.item.ua.engine.version }}</td>
              <td>{{ $d($moment(props.item.attempt_time), 'longNumeric') }}</td>
              <td class="text-xs-right">
                <v-icon :class="props.item.login_valid ? 'green--text' : 'red--text'">{{ props.item.login_valid ? 'check_circle' : 'error' }}</v-icon>
              </td>
            </tr>
          </template>
          <template slot="expand" slot-scope="props">
            <v-card flat>
              <v-card-text>{{ props.item.user_agent }}</v-card-text>
            </v-card>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-btn flat block color="blue" @click="$emit('close')">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'AccessAttemptDialog',

  props: {
    visible: {
      type: Boolean,
      default: false
    },
    attempts: Array
  },

  data () {
    return {
      headers: [
        { text: this.$t('label.ip-address'), value: 'ip_address' },
        { text: this.$t('label.os'), value: 'ua.os.name' },
        { text: this.$t('label.browser'), value: 'ua.browser.name' },
        { text: this.$t('label.engine'), value: 'ua.engine.name' },
        { text: this.$t('label.date-and-time'), value: 'attempt_time' },
        { text: this.$t('label.login'), align: 'right', value: 'login_valid' }
      ],
      items: []
    }
  }
}
</script>
