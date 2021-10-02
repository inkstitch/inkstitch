<template>
  <v-card flat>
    <v-card-title>Zigzag Underlay</v-card-title>
    <params-table>
      <param-row v-bind:value.sync="params.zigzag_underlay_inset_mm" :changed.sync="changed.zigzag_underlay_inset_mm" unit="mm">
        <translate>Zigzag underlay inset amount</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Shrink the outline, to prevent the underlay from showing around the outside of the satin column.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.zigzag_underlay_max_stitch_length_mm" :changed.sync="changed.zigzag_underlay_max_stitch_length_mm" unit="mm">
        <translate>Maximum stitch length</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Split stitch if distance of maximum stitch length is exceeded.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.zigzag_underlay_spacing_mm" :changed.sync="changed.zigzag_underlay_spacing_mm" unit="mm">
        <translate>Zig-Zag spacing (peak-to-peak)</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Distance between peaks of the zig-zags.</translate>
          </p>
        </template>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "SatinStitchZigzagUnderlayTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
