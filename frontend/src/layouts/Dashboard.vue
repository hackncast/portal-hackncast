<template>
  <div>
    <inside-nav-bar />
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

export default {
  components: { InsideNavBar }
}
</script>
