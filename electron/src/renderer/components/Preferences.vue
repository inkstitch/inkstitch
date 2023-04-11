<!--

  Authors: see git history

  Copyright (c) 2010 Authors
  Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

-->

<template>
  <v-card elevation="8" rounded="lg" class="preferences-card">
    <v-card-title class="text-center justify-center py-6">
      <h1 class="font-weight-bold text-h2 text-basil">
        Ink/Stitch Settings
      </h1>
    </v-card-title>

    <v-card-text>
      <v-tabs v-model="tab" bg-color="transparent" class="text-primary" grow>
        <v-tab key="this_svg_settings">
          This SVG
        </v-tab>
        <v-tab key="global_settings">
          Global
        </v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item key="this_svg_settings">
          <v-card flat>
            <v-card-text>
              <table>
                <tr>
                  <td class="label">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ props }">
                        <label for="collapse_len_mm" v-bind="props"><translate>Minimum jump stitch length</translate></label>
                      </template>
                      <label for="collapse_len_mm"><translate>Jump stitches smaller than this will be treated as normal stitches.</translate></label>
                    </v-tooltip>
                  </td>
                  <td class="preference">
                    <v-text-field hide-details id="collapse_len_mm" @change="updateSettings" v-model.number="this_svg_settings.collapse_len_mm" type="number"></v-text-field>
                  </td>
                  <td class="unit">
                    mm
                  </td>
                  <td class="button">
                    <v-btn small @click="setDefault('collapse_len_mm')">
                      <translate>set as default</translate>
                    </v-btn>
                  </td>
                </tr>
                <tr>
                  <td class="label">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ props }">
                        <label for="min_stitch_len_mm" v-bind="props"><translate>Minimum stitch length</translate></label>
                      </template>
                      <label for="min_stitch_len_mm"><translate>Drop stitches smaller than this value.</translate></label>
                    </v-tooltip>
                  </td>
                  <td class="preference">
                    <v-text-field hide-details id="min_stitch_len_mm" @change="updateSettings" v-model.number="this_svg_settings.min_stitch_len_mm" type="number"></v-text-field>
                  </td>
                  <td class="unit">
                    mm
                  </td>
                  <td class="button">
                    <v-btn small @click="setDefault('min_stitch_len_mm')">
                      <translate>set as default</translate>
                    </v-btn>
                  </td>
                </tr>
              </table>
            </v-card-text>
          </v-card>
        </v-window-item>
        <v-window-item key="global_settings">
          <v-card flat>
            <v-card-text>
              <table>
                <tr>
                  <td>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ props }">
                        <label for="default_collapse_len_mm" v-bind="props"><translate>Default minimum jump stitch length</translate></label>
                      </template>
                      <label for="default_collapse_len_mm"><translate>Used for new SVGs.</translate></label>
                    </v-tooltip>
                  </td>
                  <td class="preference">
                    <v-text-field hide-details id="default_min_stitch_len_mm" @change="updateSettings"  v-model.number="global_settings.default_collapse_len_mm" type="number"></v-text-field>
                  </td>
                  <td class="unit">
                    mm
                  </td>
                </tr>
                <tr>
                  <td>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ props }">
                        <label for="default_min_stitch_len_mm" v-bind="props"><translate>Default minimum stitch length</translate></label>
                      </template>
                      <label for="default_min_stitch_len_mm"><translate>Used for new SVGs.</translate></label>
                    </v-tooltip>
                  </td>
                  <td class="preference">
                    <v-text-field hide-details id="default_min_stitch_len_mm" @change="updateSettings"  v-model.number="global_settings.default_min_stitch_len_mm" type="number"></v-text-field>
                  </td>
                  <td class="unit">
                    mm
                  </td>
                </tr>
                <tr>
                  <td>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ props }">
                        <label for="cache_size" v-bind="props"><translate>Stitch plan cache size</translate></label>
                      </template>
                      <label for="default_min_stitch_len_mm"><translate>The greater the number, the more stitch plans can be cached, speeding up stitch plan calculation.  Default: 100</translate></label>
                    </v-tooltip>
                  </td>
                  <td class="preference">
                    <v-text-field hide-details id="cache_size" @change="updateSettings"  v-model.number="global_settings.cache_size" type="number"></v-text-field>
                  </td>
                  <td class="unit">
                    MB
                  </td>
                  <td class="button">
                    <v-btn small @click="clearCache"><translate>clear stitch plan cache</translate></v-btn>
                  </td>
                </tr>
              </table>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </v-card-text>
    <v-card-actions>
      <v-btn text color="primary" @click="close"><translate>done</translate></v-btn>
    </v-card-actions>
  </v-card>

</template>

<script>
import { inkStitch } from '../../lib/api.js'
export default {
  name: "Preferences",
  data: function () {
    return {
      tab: "this_svg_settings",
      this_svg_settings: {
        collapse_len_mm: null,
        min_stitch_len_mm: null,
      },
      global_settings: {
        default_min_stitch_len_mm: null,
        default_collapse_len_mm: null,
        cache_size: null
      }
    }
  },
  created: function () {
    inkStitch.get("preferences/").then(response => {
      Object.assign(this.this_svg_settings, response.data.this_svg_settings)
      Object.assign(this.global_settings, response.data.global_settings)
    })
  },
  methods: {
    setDefault(preference_name) {
      console.log(`set default: ${preference_name}`)
      this.global_settings[`default_${preference_name}`] = this.this_svg_settings[preference_name]
      this.updateSettings()
    },
    updateSettings() {
      console.log(this.this_svg_settings)
      console.log(this.global_settings)
      inkStitch.post("preferences/", {
        this_svg_settings: this.this_svg_settings,
        global_settings: this.global_settings
      }).then(response => {
        console.log(response)
      })
    },
    clearCache() {
      inkStitch.post("preferences/clear_cache").then(response => {
        console.log(response)
      })
    },
    close() {
      window.close()
    }
  }
}
</script>

<style scoped>
.preferences-card {
  margin-left: 20%;
  margin-right: 20%;
  margin-top: 5%;
}

td.label {
  vertical-align: bottom;
}

td.preference {
  padding-right: 4px;
  padding-left: 16px;
  max-width: 100px;
}

td.preference :deep(input) {
  text-align: right;
}

td.unit {
  vertical-align: bottom;
}

td.button {
  vertical-align: bottom;
  padding-left: 12px;
}
</style>
