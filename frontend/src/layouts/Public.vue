<template>
  <v-app id="app" dark>
    <v-content>
      <slot></slot>
    </v-content>
    <v-footer color="transparent" style="z-index: 2">
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>
