<template>
  <div>
    <inside-nav-bar />
    <side-bar />
    <v-content>
      <v-container fill-height fluid>
        <transition name="fade" mode="out-in">
          <slot />
        </transition>
      </v-container>
    </v-content>
  </div>
</template>

<script>
// import SideBar from '@/components/SideBar'
import InsideNavBar from '@/components/InsideNavBar'
import SideBar from '@/components/Sidebar'

export default {
  components: { InsideNavBar, SideBar }
}
</script>

<style>
.v-navigation-drawer__border {
	display: none;
}
</style>
