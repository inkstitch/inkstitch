<template>
  <v-card raised rounded="lg" class="preferences-card">
    <v-card-title class="text-center justify-center py-6">
      <h1 class="font-weight-bold text-h2 basil--text">
        Ink/Stitch Settings
      </h1>
    </v-card-title>

    <v-card-text>
      <v-tabs v-model="tab" background-color="transparent" grow>
        <v-tab key="this_svg_settings">
          This SVG
        </v-tab>
        <v-tab key="global_settings">
          Global
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab">
        <v-tab-item key="this_svg_settings">
          <v-card flat>
            <v-card-text>
              <table>
                <tr>
                  <td class="label">
                    <v-tooltip bottom>
                      <template v-slot:activator="{on, attrs}">
                        <label for="collapse_len_mm" v-on="on" v-bind="attrs"><translate>Minimum jump stitch length</translate></label>
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
                    <v-btn small @click="set_default('collapse_len_mm')"><translate>set as default</translate></v-btn>
                  </td>
                </tr>
                <tr>
                  <td class="label">
                    <v-tooltip bottom>
                      <template v-slot:activator="{on, attrs}">
                        <label for="min_stitch_len_mm" v-on="on" v-bind="attrs"><translate>Minimum stitch length</translate></label>
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
                    <v-btn small @click="set_default('min_stitch_len_mm')"><translate>set as default</translate></v-btn>
                  </td>
                </tr>
              </table>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item key="global_settings">
          <v-card flat>
            <v-card-text>
              <table>
                <tr>
                  <td>
                    <v-tooltip bottom>
                      <template v-slot:activator="{on, attrs}">
                        <label for="default_collapse_len_mm" v-on="on" v-bind="attrs"><translate>Default minimum jump stitch length</translate></label>
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
                      <template v-slot:activator="{on, attrs}">
                        <label for="default_min_stitch_len_mm" v-on="on" v-bind="attrs"><translate>Default minimum stitch length</translate></label>
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
                      <template v-slot:activator="{on, attrs}">
                        <label for="cache_size" v-on="on" v-bind="attrs"><translate>Stitch plan cache size</translate></label>
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
        </v-tab-item>
      </v-tabs-items>
    </v-card-text>
    <v-card-actions>
      <v-btn text color="primary" @click="close"><translate>done</translate></v-btn>
    </v-card-actions>
  </v-card>

</template>

<script>
const inkStitch = require("../../lib/api")

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

td.preference::v-deep input {
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
