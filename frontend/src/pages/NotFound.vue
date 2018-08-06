<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <img src="@/assets/glider-transluscent.svg"
             style="width: 150px"
             class="mb-5 in-dark"
             />
        <div style="text-align: center">
          <h1>404 - Page Not Found</h1>
          <p>Sorry, the page you were looking for could not be found!</p>
        </div>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound',

  route: {
    name: 'not-found',
    layout: 'Public'
  }
}
</script>

<style lang="sass" scoped>
img
  &.in-dark
    opacity: .7
</style>
