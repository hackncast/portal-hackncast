<template>
  <v-card>
    <v-toolbar flat absolute dense :class="[cardNavClass]">
      <v-toolbar-title>{{ user.fullName }}</v-toolbar-title>
    </v-toolbar>

    <v-card-media height="200px" :src="user.avatar" />

    <v-card-title class="pa-0">
      <v-list style="width: 100%">
        <v-list-tile class="pt-1">
          <v-list-tile-content>
            <v-list-tile-title>Username</v-list-tile-title>
            <v-list-tile-sub-title>{{ user.username }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile class="pt-1">
          <v-list-tile-content>
            <v-list-tile-title>Email</v-list-tile-title>
            <v-list-tile-sub-title>{{ user.email }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile class="pt-1">
          <v-list-tile-content>
            <v-list-tile-title>Groups <span v-if="activeGroups.length > 0">({{ activeGroups.length}})</span></v-list-tile-title>
            <v-list-tile-sub-title>{{ activeGroups.map(g => g.name).join(', ') | defaultValue('-') }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn icon ripple @click="showGroupsDialog = true"><v-icon color="grey lighten-1">edit</v-icon></v-btn>
          </v-list-tile-action>
        </v-list-tile>

        <v-list-tile class="pt-1">
          <v-list-tile-content>
            <v-list-tile-title>Is Staff</v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-action style="position: relative">
            <v-switch class="v-switch--right" v-model="user.isStaff" @click.stop="setAsAdmin(user)" />
          </v-list-tile-action>
        </v-list-tile>

        <v-list-tile class="pt-1">
          <v-list-tile-content>
            <v-list-tile-sub-title>Last Login: {{ user.lastLogin | fmtRelativeDate | defaultValue('Never') }}</v-list-tile-sub-title>
            <v-list-tile-sub-title>Joined at {{ user.dateJoined | fmtDate }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>

      </v-list>
    </v-card-title>

    <v-divider />

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat color="red" @click="blockUser(user)">{{ user.isActive ? 'Block' : 'Unblock' }}</v-btn>
    </v-card-actions>

    <user-list-groups-dialog v-model="showGroupsDialog" @close="showGroupsDialog = false" :user="user" />
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import UserListGroupsDialog from '@/components/manage/UserListGroupsDialog'

export default {
  name: 'ManageUserListItem',

  components: { UserListGroupsDialog },

  data () {
    return {
      showGroupsDialog: false
    }
  },

  props: {
    user: {
      type: Object
    }
  },

  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser'
    }),

    cardNavClass () {
      return this.$store.state.ui.darkTheme ? 'card--nav--dark' : 'card--nav--light'
    },

    activeGroups () {
      return this.user.groups.filter(g => g.participates === true)
    }
  },

  methods: {
    ...mapActions({
      updateUser: 'manage/updateUser'
    }),

    setAsAdmin (user) {
      const userData = { pk: user.pk, is_staff: !user.isStaff }
      this.updateUser(userData)
        .then(user => {
          if (user.isStaff) {
            this.$toast({ text: `${user.fullName} is now an staff member.` })
          } else {
            this.$toast({ text: `${user.fullName} is no longer a staff member.` })
          }
        })
        .catch(err => {
          this.$toast({
            text: `An error ocurred while trying to add ${user.fullName} as a staff member.`,
            color: 'error'
          })
          throw err
        })
    },

    blockUser (user) {
      const userData = { pk: user.pk, is_active: !user.isActive }
      this.updateUser(userData)
        .then(user => {
          if (user.isActive) {
            this.$toast({ text: `${user.fullName} is now unblocked.` })
          } else {
            this.$toast({ text: `${user.fullName} is now blocked.` })
          }
        })
        .catch(err => {
          this.$toast({ text: `An error ocurred while trying to block ${user.fullName}.`, color: 'error' })
          throw err
        })
      return false
    }
  }
}
</script>

<style lang="sass">
.card--nav--dark
  background-color: rgba(0, 0, 0, .3) !important

.card--nav--light
  background-color: rgba(255, 255, 255, .3) !important

.v-switch--right
  position: absolute
  right: 0px
  .v-input--selection-controls__input
    margin-right: 0px !important

</style>
