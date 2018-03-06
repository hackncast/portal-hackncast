<template>
<v-tabs icons-and-text centered dark style="margin-top: 12px" :color="color">
  <v-tabs-slider :color="sliderColor"></v-tabs-slider>
  <v-tab exact :to="{ name: 'user:profile' }">account <v-icon>account_box</v-icon></v-tab>
  <v-tab exact :to="{ name: 'user:profile:emails' }">emails <v-icon>email</v-icon></v-tab>
  <v-tab exact :to="{ name: 'user:profile:passwords' }">passwords <v-icon>security</v-icon></v-tab>
</v-tabs>
</template>

<script>
export default {
  name: 'UserProfileNavbar',

  props: {
    color: { type: String },
    sliderColor: { type: String }
  }
}
</script>
