<template>
  <v-navigation-drawer fixed clipped app :mini-variant-width="55" :mini-variant="mini" :class="[inDesktop ? 'transparent' : '']" v-model="sidebarState">
    <v-list dense v-if="mini">
      <template v-for="item in items">
        <v-tooltip :key="item.title" right>
          <template v-if="!item.items">
            <v-list-tile exact color="grey" :to="item.url" slot="activator" :active-class="activeClass">
              <v-icon color="grey">{{ item.icon }}</v-icon>
            </v-list-tile>
          </template>
          <template v-else>
            <v-menu top offset-y transition="slide-y-transition" offset-x slot="activator">
              <v-list-tile colo="grey" slot="activator" @click="nothing" :active-class="activeClass">
                <v-icon color="grey">{{ item.icon }}</v-icon>
              </v-list-tile>
              <v-list>
                <v-list-tile exact v-for="subItem in item.items" :key="subItem.title" :to="subItem.url" :active-class="activeClass">
                  <v-list-tile-action v-if="subItem.icon">
                    <v-icon>{{ subItem.icon }}</v-icon>
                  </v-list-tile-action>
                  <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
          </template>
        <span>{{ item.title }}</span>
        </v-tooltip>
      </template>
    </v-list>

    <v-list dense v-else>
      <template v-for="item in items">
        <template v-if="!item.items">
          <v-list-tile ripple exact color="grey" :to="item.url" :key="item.title" :active-class="activeClass">
            <v-list-tile-action>
              <v-icon color="grey">{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
        <template v-else>
          <v-list-group v-model="item.active" :key="item.title" :prepend-icon="item.icon" :active-class="activeClass" no-action>
            <v-list-tile color="grey" slot="activator" :active-class="activeClass">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile ripple exact color="grey" v-for="subItem in item.items" :key="subItem.title" :to="subItem.url" :active-class="activeClass">
              <v-list-tile-content>
                <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-icon color="grey">{{ subItem.icon }}</v-icon>
              </v-list-tile-action>
            </v-list-tile>
          </v-list-group>
        </template>
      </template>
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
          icon: 'home',
          title: 'Home',
          url: {name: 'home'}
        },
        {
          icon: 'settings',
          title: 'Administration',
          items: [
            { title: 'Vaults', icon: 'https' },
            { title: 'Users', icon: 'person', url: {name: 'manage-users'} },
            { title: 'Groups', icon: 'people' }
          ]
        }
      ]
    }
  },

  computed: {
    sidebarState: {
      get () { return this.$store.state.ui.sidebarVisible },
      set (val) { this.$store.dispatch('ui/showSidebar', val) }
    },

    mini: {
      get () { return this.$store.state.ui.miniSidebar && this.$vuetify.breakpoint.lgAndUp },
      set (val) { this.$store.dispatch('ui/setMiniSidebar', val) }
    },

    activeClass () {
      if (this.$store.state.ui.darkTheme) {
        return 'white--text'
      }
      return 'black--text'
    }
  },

  watch: {
    '$vuetify.breakpoint.lgAndUp' (to) { this.checkSidebarMode(to) }
  },

  methods: {
    checkSidebarMode (lgAndUp) {
      this.inDesktop = lgAndUp
      this.$store.dispatch('ui/showSidebar', lgAndUp)
    },

    nothing () {}
  },

  created () { this.checkSidebarMode(this.$vuetify.breakpoint.lgAndUp) }
}
</script>

<style>
.v-navigation-drawer__border {
  display: none;
}
</style>
