<template>
  <div class="overlay overlay--active" style="z-index: 201;">
    <v-progress-circular
      style="position: absolute; top: calc(50% - 50px/2); left: calc(50% - 50px/2);"
      indeterminate color="blue lighten-5"
      size="50"/>
  </div>
</template>

<script>
export default {
  name: 'LoadingDialog'
}
</script>
