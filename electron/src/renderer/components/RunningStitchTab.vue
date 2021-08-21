<template>
  <v-card flat>
    <params-table>
      <param-row v-bind:value.sync="params.manual_stitch_placement" :changed.sync="changed.manual_stitch_placement" type="checkbox">
        <translate>Manual stitch placement</translate>
        <template v-slot:tooltip>
          <translate>Stitch every node in the path. Stitch length and zig-zag spacing are ignored.</translate>
        </template>
      </param-row>
      <param-row v-bind:value.sync="params.running_stitch_length" :changed.sync="changed.running_stitch_length" unit="mm">
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
          </translate>
        </template>
      </param-row>

    </params-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../../lib/mixins'
import ParamsTable from './ParamsTable.vue'
import ParamRow from './ParamRow.vue'

export default {
  name: 'RunningStitchTab',
  components: {
    ParamsTable,
    ParamRow
  },
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      "params": {
        manual_stitch_placement: null,
        running_stitch_length: null,
        bean_stitch_repeats: null
      },
      changed: {
        manual_stitch_placement: false,
        running_stitch_length: false,
        bean_stitch_repeats: false
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
