<template>
  <v-card flat>
    <v-card-title>
      Manual Stitch
    </v-card-title>
    <v-card-text>
      <v-checkbox v-on:change="$emit('disable-manual-stitch')" checked :label="$gettext('manual stitch mode')"></v-checkbox>
    </v-card-text>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../../lib/mixins'

export default {
  name: "ManualStitchTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
