<template>
  <v-layout row justify-center>
    <v-dialog persistent v-model="value" scrollable max-width="300px">
      <v-card>
        <v-card-title>Avaiable Groups for {{ user.displayName }}</v-card-title>
        <v-divider />
        <v-card-text style="max-height: 300px;">
          <v-checkbox
            hide-details
            class="mt-0"
            v-for="group in user.groups"
            v-model="selected"
            :key="group.pk"
            :label="group.name"
            :value="group.pk"
            />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn color="green darken-1" flat :disabled="loading" @click.native="$emit('close')">Back</v-btn>
          <v-spacer />
          <v-btn depressed color="blue darken-1 white--text" :loading="loading" @click.native="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data () {
    return {
      selected: [],
      loading: false
    }
  },

  props: {
    user: { type: Object },
    value: { type: Boolean, default: false }
  },

  watch: {
    value (val) {
      if (!val) return
      this.loading = false
      this.selected.empty()
      this.user.groups.filter(g => g.participates).forEach(g => {
        this.selected.push(g.pk)
      })
    }
  },

  methods: {
    ...mapActions({
      updateUser: 'manage/updateUser'
    }),

    saveUser () {
      this.loading = true
      const userData = { pk: this.user.pk, groups: this.selected }
      this.updateUser(userData)
        .then(user => {
          this.$toast({ text: `Groups updated successfully!` })
        })
        .catch(err => {
          this.$toast({ text: "Sorry, I could't update the group list!", color: 'error' })
          throw err
        })
        .finally(() => {
          this.loading = false
          this.$emit('close')
        })
    }
  }
}
</script>
