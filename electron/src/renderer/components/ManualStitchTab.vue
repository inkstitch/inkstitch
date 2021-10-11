<template>
  <v-card flat>
    <v-card-title>
      Manual Stitch
    </v-card-title>
    <v-card-text>
      <v-checkbox v-on:change="$emit('disable-manual-stitch')" v-model="checked" :label="$gettext('manual stitch mode')"></v-checkbox>
    </v-card-text>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "ManualStitchTab",
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      checked: true
    }
  }
}
</script>

<style scoped>

</style>
