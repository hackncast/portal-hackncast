<template>
  <v-app id="app" dark :style="{ backgroundImage: getbackgroundImage }">
    <v-toolbar flat color="transparent" style="z-index: 2" id="nav-site-title">
      <v-toolbar-side-icon tab-index="-1">
        <v-avatar>
          <img src="@/assets/hnc-logo-noframe-inverted.svg" alt="Logo">
        </v-avatar>
      </v-toolbar-side-icon>
      <v-toolbar-title class="hnc-title" style="font-size: 2em; padding-bottom: 5px;">Hack'n'Cast</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </v-content>
    <v-footer color="transparent" style="z-index: 2">
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'OutsideLayout',

  data () {
    return {
      images: [
        // 'https://cdn.stocksnap.io/img-thumbs/960w/CWYK8CLC61.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/DKNN0YHNEE.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/U3W2SHOLWQ.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/4GO4VAB14Z.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/YSUCTBXV32.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/BKWZJHXR57.jpg',
        'https://cdn.stocksnap.io/img-thumbs/960w/YP10KAYY2D.jpg',
        'https://cdn.stocksnap.io/img-thumbs/960w/Z7L87CLJVN.jpg'
      ]
    }
  },

  computed: {
    getbackgroundImage () {
      let image = this.images[Math.floor(Math.random() * this.images.length)]
      return `url('${image}')`
    }
  }
}
</script>

<style scoped>
#app {
  background-size: cover;
  background-position: center;
}
#app::before {
  background-color: rgba(0, 0, 0, .6);
  position: fixed;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: block;
  left: 0;
  top: 0;
  content: "";
}

@media screen and (max-width: 600px) {
  #nav-site-title .toolbar__title {
    width: 100%;
    text-align: center;
    margin-left: -36px;
  }
}

@media screen and (min-width: 600px) {
  #nav-site-title {
    margin-left: 8%;
    margin-right: 8%;
  }
}
</style>
