<template>
  <private-layout>
      <v-content>
        <v-container fill-height fluid>
          <transition name="fade" mode="out-in">
            <slot />
          </transition>
        </v-container>
      </v-content>
  </private-layout>
</template>

<script>
import PrivateLayout from '@/layouts/Private'
// import SideBar from '@/components/SideBar'
// import InsideNavBar from '@/components/InsideNavBar'

export default {
  components: { PrivateLayout }
}
</script>
