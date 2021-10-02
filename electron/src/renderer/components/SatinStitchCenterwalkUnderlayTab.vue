<template>
  <v-card flat>
    <v-card-title>Center-walk Underlay</v-card-title>
    <params-table>
      <param-row v-bind:value.sync="params.center_walk_underlay_stitch_length_mm" :changed.sync="changed.center_walk_underlay_stitch_length_mm" unit="mm">
        <translate>Stitch length</translate>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "SatinStitchCenterwalkUnderlayTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
