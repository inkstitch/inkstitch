<template>
  <v-card flat>
    <v-card-text>
      <v-card class="pa-2">
        <params-table>
          <param-row v-bind:value.sync="params.running_stitch_length" :changed.sync="changed.running_stitch_length_mm" unit="mm">
            <translate>Running stitch length</translate>
          </param-row>
          <param-row v-bind:value.sync="params.bean_stitch_repeats" :changed.sync="changed.bean_stitch_repeats" type="checkbox">
            <translate>Bean stitch number of repeats</translate>
            <template v-slot:tooltip>
              <p>
                <translate>Backtrack each stitch this many times.</translate>
              </p>
              <p>
                <translate>A value of 1 would triple each stitch (forward, back, forward).</translate>
              </p>
              <p>
                <translate>A value of 2 would quintuple each stitch, etc.</translate>
              </p>
            </template>
          </param-row>
          <param-row v-bind:value.sync="params.repeats" :changed.sync="changed.repeats" type="text">
            <translate>Repeats</translate>
            <template v-slot:tooltip>
              <translate>Defines how many times to run down and back along the path.</translate>
            </template>
          </param-row>
        </params-table>
      </v-card>
    </v-card-text>
    <params-table>
      <param-row v-bind:value.sync="params.manual_stitch_placement" :changed.sync="changed.manual_stitch_placement" type="checkbox">
        <translate>Manual stitch placement</translate>
        <template v-slot:tooltip>
          <translate>Stitch every node in the path. All settings above are ignored.</translate>
        </template>
      </param-row>
    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: 'RunningStitchTab',
  element_type: "running_stitch",
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      "params": {
        manual_stitch_placement: null,
        running_stitch_length_mm: null,
        bean_stitch_repeats: null,
        repeats: null
      },
      changed: {
        manual_stitch_placement: false,
        running_stitch_length_mm: false,
        bean_stitch_repeats: false,
        repeats: false
      }
    }
  },
  watch: {
    'params.manual_stitch_placement': function () {
      /* Manual stitch is special (see Params.py) */
      console.log("saw change")
      this.$emit('enable-manual-stitch')
    }
  }
}
</script>

<style scoped>

.params-tab-input::v-deep .v-input__control {
  max-width: 100px !important;
}

.params-tab-input-label {
  flex-grow: 1;
}

td {
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 2px;
  padding-bottom: 2px;
}
</style>
