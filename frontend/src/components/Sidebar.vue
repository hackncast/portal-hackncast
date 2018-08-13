<template>
  <v-navigation-drawer fixed clipped app :mini-variant.sync="mini" :class="[inDesktop ? 'transparent' : '']" v-model="sidebarState">
    <v-list dense>
      <v-list-tile @click="$router.push({name: 'home'})">
        <v-list-tile-action>
          <v-icon>home</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Home</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>

      <v-list-group
        v-for="item in items"
        v-model="item.active"
        :key="item.title"
        :prepend-icon="item.action"
        no-action
        >

        <v-list-tile slot="activator">
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile
          v-for="subItem in item.items"
          :key="subItem.title"
          @click=""
          >
          <v-list-tile-content>
            <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-icon>{{ subItem.action }}</v-icon>
          </v-list-tile-action>
        </v-list-tile>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data () {
    return {
      inDesktop: true,
      items: [
        {
          action: 'settings',
          title: 'Administration',
          items: [
            { title: 'Vaults' },
            { title: 'Users' },
            { title: 'Groups' }
          ]
        }
      ]
    }
  },

  computed: {
    sidebarState: {
      get () { return this.$store.state.ui.sidebarVisible },
      set (val) { this.$store.dispatch('ui/showSidebar', val) }
    }
  },

  watch: {
    '$vuetify.breakpoint.lgAndUp' (to) { this.checkSidebarMode(to) }
  },

  methods: {
    checkSidebarMode (lgAndUp) {
      this.inDesktop = lgAndUp
      this.$store.dispatch('ui/showSidebar', lgAndUp)
    }
  },

  created () { this.checkSidebarMode(this.$vuetify.breakpoint.lgAndUp) }
}
</script>
