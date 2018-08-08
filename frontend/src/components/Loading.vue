<template functional>
  <div class="overlay overlay--active" style="z-index: 201;">
    <v-progress-circular
      style="position: absolute; top: calc(50% - 50px/2); left: calc(50% - 50px/2);"
      indeterminate color="blue lighten-5"
      size="50"/>
  </div>
</template>

<style lang="scss">
.overlay {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
}
</style>
