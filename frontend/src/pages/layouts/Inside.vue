<template>
  <v-app id="inspire">
    <inside-nav-bar/>
    <side-bar/>
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
          <transition name="fade" mode="out-in">
            <router-view />
          </transition>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import InsideNavBar from '@/components/InsideNavBar'
import SideBar from '@/components/SideBar'

export default {
  components: {InsideNavBar, SideBar}
}
</script>
