<template>
  <v-container fluid>
    <p>Home</p>
    <p>
      <router-link :to="{name: 'auth-login'}">Login</router-link>
    </p>
    <p>
      <router-link :to="{name: 'auth-registration'}">Registration</router-link>
    </p>
  </v-container>
</template>

<script>
export default {
  name: 'Home',

  route: {
    name: 'home',
    layout: 'Public',
    middlewares: ['PrivateOnly']
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
