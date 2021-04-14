<!--

  Authors: see git history

  Copyright (c) 2010 Authors
  Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

-->

<template>
  <v-dialog max-width="500px" value="true">
    <v-card v-if="step == 'pick'" key="pick" rounded="lg" :loading="installing" :disabled="installing">
      <v-card-title>
        <translate>
          Install Palettes
        </translate>
      </v-card-title>
      <v-card-text class="text--primary">
        <translate>Ink/Stitch can install palettes for Inkscape matching the thread colors from popular machine embroidery thread manufacturers.
        </translate>
      </v-card-text>
      <v-file-input class="mb-3 mx-3" webkitdirectory hide-details v-model="path" truncate-length="45"
                    :label="$gettext('Choose Inkscape directory')">
      </v-file-input>
      <v-card-text>
        <translate>If you are not sure which file path to choose, click on install directly. In most cases Ink/Stitch will guess the correct path.
        </translate>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="primary" v-on:click="install">
          <v-icon>mdi-palette</v-icon>
          <translate>Install</translate>
        </v-btn>
        <v-btn text color="primary" v-on:click="close">
          <translate>Cancel</translate>
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card v-if="step == 'done'" key="done">
      <v-card-title>
        <translate>
          Installation Completed
        </translate>
      </v-card-title>
      <v-card-text class="text--primary">
        <translate>
          Inkscape palettes have been installed. Please restart Inkscape to load the new palettes.
        </translate>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="primary" v-on:click="close">
          Done
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card v-if="step == 'error'" key="error">
      <v-card-title>
        <translate>
          Installation Failed
        </translate>
      </v-card-title>
      <v-card-text class="text--primary">
        <translate>Inkscape add-on installation failed</translate>
      </v-card-text>
      <v-card-text class="text--secondary">
        {{ error }}
      </v-card-text>
      <v-card-actions>
        <v-btn text color="primary" v-on:click="retry">
          <translate>Try again</translate>
        </v-btn>
        <v-btn text color="primary" v-on:click="close">
          <translate>Cancel</translate>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
const inkStitch = require("../../lib/api")

export default {
  name: "InstallPalettes",
  data: function () {
    return {
      path: null,
      installing: false,
      step: "pick",
      error: null
    }
  },
  methods: {
    install() {
      this.installing = true
      inkStitch.post('install/palettes', {path: this.path.path || this.path.name}).then(response => {
        this.step = "done"
      }).catch(error => {
        this.step = "error"
        this.error = error.response.data.error
      }).then(() => {
        this.installing = false
      })
    },
    close() {
      window.close()
    },
    retry() {
      this.installing = false
      this.step = "pick"
    }
  },
  created: function () {
    inkStitch.get("install/default-path").then(response => {
      this.path = new File([""], response.data, {})
    })
  }
}
</script>

<style scoped>

</style>
