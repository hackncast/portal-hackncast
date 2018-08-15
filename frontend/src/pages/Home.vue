<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <img src="@/assets/glider-transluscent.svg"
             style="width: 150px"
             class="mb-5"
             :class="[ $store.state.ui.darkTheme ? 'in-dark' : 'in-light' ]"
             />
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
export default {
  name: 'Home',

  route: {
    name: 'home',
    layout: 'Dashboard',
    middlewares: ['PrivateOnly'],
    breadcrumbs: [
      {title: 'Dashboard'}
    ]
  }
}
</script>

<style lang="sass" scoped>
img
  &.in-dark, &.in-light
    transition: all 1s ease

  &.in-dark
    opacity: .2

  &.in-light
    filter: contrast(.7)
</style>
