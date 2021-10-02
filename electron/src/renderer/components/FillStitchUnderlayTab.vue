<template>
  <v-card flat>
    <v-card-title>Underlay</v-card-title>
    <params-table>
      <param-row v-bind:value.sync="params.fill_underlay_angle" :changed.sync="changed.fill_underlay_angle" unit="deg">
        <translate>Fill Angle</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Default: fill angle + 90 deg. Insert comma-seperated list for multiple layers.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.fill_underlay_inset_mm" :changed.sync="changed.fill_underlay_inset_mm" unit="mm">
        <translate>Inset</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Shrink the shape before doing underlay, to prevent underlay from showing around the outside of the fill.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.fill_underlay_max_stitch_length_mm" :changed.sync="changed.fill_underlay_max_stitch_length_mm" unit="mm">
        <translate>Max stitch length</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Default: equal to fill max stitch length.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.fill_underlay_row_spacing_mm" :changed.sync="changed.fill_underlay_row_spacing_mm" unit="mm">
        <translate>Row spacing</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Default: 3x fill row spacing.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.fill_underlay_skip_last" :changed.sync="changed.fill_underlay_skip_last" type="checkbox">
        <translate>Skip last stitch in each row</translate>
        <template v-slot:tooltip>
          <p>
            <translate>The last stitch in each row is quite close to the first stitch in the next row.</translate>
          </p>
          <p>
             <translate>Skipping it decreases stitch count and density.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.underlay_underpath" :changed.sync="changed.underlay_underpath" type="checkbox">
        <translate>Underpath</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Travel inside the shape when moving from section to section.</translate>
          </p>
          <p>
             <translate>Underpath stitches avoid traveling in the direction of the row angle so that they are not visible.</translate>
          </p>
          <p>
             <translate>This gives them a jagged appearance.</translate>
          </p>
        </template>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "FillStitchUnderlayTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
