<template>
  <v-card flat>
    <v-card-title>Fill Stitch</v-card-title>
    <params-table>
      <param-row v-bind:value.sync="params.angle" :changed.sync="changed.angle" unit="deg">
        <translate>Angle of lines of stitches</translate>
        <template v-slot:tooltip>
          <p>
            <translate>The angle increases in a counter-clockwise direction.
                       0 is horizontal.  Negative angles are allowed.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.expand_mm" :changed.sync="changed.expand_mm" unit="mm">
        <translate>Expand</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Expand the shape before fill stitching, to compensate for gaps between shapes.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.max_stitch_length_mm" :changed.sync="changed.max_stitch_length_mm" unit="mm">
        <translate>Maximum fill stitch length</translate>
        <template v-slot:tooltip>
          <p>
            <translate>The length of each stitch in a row.  Shorter stitch may be used at the start or end of a row.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.row_spacing_mm" :changed.sync="changed.row_spacing_mm" unit="mm">
        <translate>Spacing between rows</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Distance between rows of stitches.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.running_stitch_length_mm" :changed.sync="changed.running_stitch_length_mm" unit="mm">
        <translate>Running stitch length (traversal between sections)</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Length of stitches around the outline of the fill region used when moving from section to section.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.skip_last" :changed.sync="changed.skip_last" type="checkbox">
        <translate>Skip last stitch in each row</translate>
        <template v-slot:tooltip>
          <p>
            <translate>The last stitch in each row is quite close to the first stitch in the next row.
                       Skipping it decreases stitch count and density.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.staggers" :changed.sync="changed.staggers" unit="int">
        <translate>Stagger rows this many times before repeating</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Setting this dictates how many rows apart the stitches will be before they fall in the same column position.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.underpath" :changed.sync="changed.underpath" type="checkbox">
        <translate>Underpath</translate>
        <template v-slot:tooltip>
          <p>
            <translate>Travel inside the shape when moving from section to section.</translate>
          </p>
          <p>
            <translate>Underpath stitches avoid traveling in the direction of the row angle so that they are not visible.</translate>
          </p>
            <translate>This gives them a jagged appearance.</translate>
          </p>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.ties" :changed.sync="changed.ties" type="select" 
                 :items="[{text: 'Both', value: '0'}, {text: 'Before', value: 1}, {text: 'After', value: 2}, {text: 'Neither', value: 3}]">
      <translate>Allow lock stitches</translate>
      <template v-slot:tooltip>
          <p>
            <translate>Tie thread at the beginning and/or end of this object.</translare>
          </p>
        </template>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: "FillStitchTab",
  mixins: [ParamsTabMixin]
}
</script>

<style scoped>

</style>
