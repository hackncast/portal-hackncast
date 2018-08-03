<template>
<v-container fluid fill-height pt-1>
  <v-layout align-center justify-center style="z-index: 2">
    <v-flex xs12 sm6 md3>
      Login
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  name: 'LoginPage',

  route: {
    name: 'auth-login',
    layout: 'Public',
    middlewares: ['PublicOnly']
  }
}
</script>
