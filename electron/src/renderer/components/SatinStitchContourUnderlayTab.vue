<template>
  <v-card flat>
    <v-card-title>Contour Underlay</v-card-title>
    <params-table>
      <param-row v-bind:value.sync="params.contour_underlay_inset_mm" :changed.sync="changed.contour_underlay_inset_mm" unit="mm">
        <translate>Contour underlay inset amount</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Shrink the outline, to prevent the underlay from showing around the outside of the satin column.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.contour_underlay_stitch_length_mm" :changed.sync="changed.contour_underlay_stitch_length_mm" unit="mm">
        <translate>Stitch length</translate>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "SatinStitchContourUnderlayTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
