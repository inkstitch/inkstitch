<template>
  <v-card flat>
    <v-card-text>
      <div class="flex-center">
        <v-radio-group v-model="params.satin_column" class="my-4" row hide-details>
          <v-radio :label="$gettext('satin column')" :value="true"></v-radio>
          <v-radio :label="$gettext('basic satin')" :value="false"></v-radio>
        </v-radio-group>
      </div>
      <v-card v-if="params.satin_column" key="satin_column_settings">
        <v-card-text class="pt-0">
          <params-table>
            <param-row v-bind:value.sync="params.zigzag_spacing_mm" :changed.sync="changed.zigzag_spacing_mm" type="text">
              <translate>Zig-zag spacing (peak-to-peak)</translate>
              <template v-slot:tooltip>
                <translate>Peak-to-peak distance between zig-zags.</translate>
              </template>
            </param-row>
            <param-row v-bind:value.sync="params.pull_compensation_mm" :changed.sync="changed.pull_compensation_mm" type="text">
              <translate>Pull compensation</translate>
              <template v-slot:tooltip>
                <p>
                  <translate>Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape.</translate>
                </p>
                <p>
                  <translate>This setting expands each pair of needle penetrations outward from the center of the satin column.</translate>
                </p>
              </template>
            </param-row>
            <param-row v-bind:value.sync="params.maximum_stitch_length_mm" :changed.sync="changed.maximum_stitch_length_mm" type="text">
              <translate>Maximum stitch length</translate>
              <template v-slot:tooltip>
                <translate>Maximum stitch length for split stitches.</translate>
              </template>
            </param-row>
            <param-row v-bind:value.sync="params.e_stitch" :changed.sync="changed.e_stitch" type="checkbox">
              <translate>E stitch</translate>
              <template v-slot:tooltip>
                <translate translate-comment="&quot;E&quot; stitch is so named because it looks like the letter E.">"E" stitch</translate>
              </template>
            </param-row>
            <param-row v-bind:value.sync="params.contour_underlay" :changed.sync="changed.contour_underlay" type="checkbox">
              <translate>Contour Underlay</translate>
              <template v-slot:tooltip>
                <translate>Contour underlay is stitching just inside the rectangular shape of the satin column; that is, up one side and down the
                  other.
                </translate>
              </template>
            </param-row>
            <tr v-if="params.contour_underlay">
              <td colspan="4">
                <params-table class="subtable">
                  <param-row v-bind:value.sync="params.contour_underlay_stitch_length_mm" :changed.sync="changed.contour_underlay_stitch_length_mm"
                             type="text">
                    <translate>Contour underlay stitch length</translate>
                  </param-row>
                  <param-row v-bind:value.sync="params.contour_underlay_inset_mm" :changed.sync="changed.contour_underlay_inset_mm"
                             type="text">
                    <translate>Contour underlay inset</translate>
                    <template v-slot:tooltip>
                      <translate>How far inside the edge of the column to stitch the underlay.</translate>
                    </template>
                  </param-row>
                </params-table>
              </td>
            </tr>
            <param-row v-bind:value.sync="params.center_walk_underlay" :changed.sync="changed.center_walk_underlay" type="checkbox">
              <translate>Center-walk underlay</translate>
              <template v-slot:tooltip>
                <translate>Center walk underlay is stitching down and back in the center-line between the two sides of the satin column.
                </translate>
              </template>
            </param-row>
            <tr v-if="params.center_walk_underlay">
              <td colspan="4">
                <params-table class="subtable">
                  <param-row v-bind:value.sync="params.center_walk_underlay_stitch_length_mm"
                             :changed.sync="changed.center_walk_underlay_stitch_length_mm"
                             type="text">
                    <translate>Center-walk underlay stitch length</translate>
                  </param-row>
                </params-table>
              </td>
            </tr>
            <param-row v-bind:value.sync="params.zigzag_underlay" :changed.sync="changed.zigzag_underlay" type="checkbox">
              <translate>Zig-zag underlay</translate>
              <template v-slot:tooltip>
                <translate>Zig-zag underlay is a loose zig-zag stitch to the end and back to the start.</translate>
              </template>
            </param-row>
            <tr v-if="params.zigzag_underlay">
              <td colspan="4">
                <params-table class="subtable">
                  <param-row v-bind:value.sync="params.zigzag_underlay_spacing_mm"
                             :changed.sync="changed.zigzag_underlay_spacing_mm"
                             type="text">
                    <translate>Zig-Zag spacing (peak-to-peak)</translate>
                    <template v-slot:tooltip>
                      <translate>Distance between peaks of the zig-zags.</translate>
                    </template>
                  </param-row>
                  <param-row v-bind:value.sync="params.zigzag_underlay_inset_mm"
                             :changed.sync="changed.zigzag_underlay_inset_mm"
                             type="text">
                    <translate>Zig-zag underlay inset</translate>
                    <template v-slot:tooltip>
                      <translate>
                        <p>
                          <translate>How far inside the edge of the column to stitch the underlay.</translate>
                        </p>
                        <p>
                          <translate>default: half of contour underlay inset</translate>
                        </p>
                      </translate>
                    </template>
                  </param-row>
                </params-table>
              </td>
            </tr>
          </params-table>
        </v-card-text>
      </v-card>
      <v-card v-else key="basic_satin_settings">
        <v-card-text class="pt-0">
          <params-table>
            <param-row v-bind:value.sync="params.zigzag_spacing_mm" :changed.sync="changed.zigzag_spacing_mm" type="text">
              <translate>Zig-zag spacing (peak-to-peak)</translate>
              <template v-slot:tooltip>
                <translate>Peak-to-peak distance between zig-zags.</translate>
              </template>
            </param-row>
          </params-table>
        </v-card-text>
      </v-card>
      <params-table>
        <param-row :value.sync="manual_stitch" :changed="false" type="checkbox">
          <translate>Manual stitch placement</translate>
          <template v-slot:tooltip>
            <translate>Stitch every node in the path. All settings above are ignored.</translate>
          </template>
        </param-row>
      </params-table>
    </v-card-text>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../lib/mixins'

export default {
  name: 'SatinStitchTab',
  element_type: 'satin_stitch',
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      params: {
        satin_column: true,
        e_stitch: null,
        maximum_stitch_length_mm: null,
        zigzag_spacing_mm: null,
        pull_compensation_mm: null,
        contour_underlay: null,
        contour_underlay_stitch_length_mm: null,
        contour_underlay_inset_mm: null,
        center_walk_underlay: null,
        center_walk_underlay_stitch_length_mm: null,
        zigzag_underlay: null,
        zigzag_underlay_spacing_mm: null,
        zigzag_underlay_inset_mm: null,
      },
      changed: {
        satin_column: false,
        e_stitch: false,
        maximum_stitch_length_mm: false,
        zigzag_spacing_mm: false,
        pull_compensation_mm: false,
        contour_underlay: false,
        contour_underlay_stitch_length_mm: false,
        contour_underlay_inset_mm: false,
        center_walk_underlay: false,
        center_walk_underlay_stitch_length_mm: false,
        zigzag_underlay: false,
        zigzag_underlay_spacing_mm: false,
        zigzag_underlay_inset_mm: false,
      },
      manual_stitch: false
    }
  },
  watch: {
    manual_stitch() {
      /* Manual stitch is special (see Params.py) */
      this.$emit('enable-manual-stitch')
    }
  }
}
</script>

<style scoped>
.subtable {
  margin-left: 16px;
}

.flex-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
