<template>
  <div>
    <v-card v-if="step == 'pick'" rounded="lg" :loading="installing" :disabled="installing" class="mx-auto my-3 pa-1" elevation=8 max-width="500px">
      <v-container>
        <v-card-title>
          <translate>
            Install Palettes
          </translate>
        </v-card-title>
        <v-card-text class="text--primary">
          <translate>Ink/Stitch can install palettes for Inkscape matching the thread colors from popular machine embroidery thread manufacturers.
          </translate>
        </v-card-text>
        <v-file-input class="mb-3" webkitdirectory hide-details v-model="path" color="rgb(0,51,153)"
                      :label="$gettext('Choose Inkscape directory')"></v-file-input>
        <v-card-actions>
          <v-btn text color="rgb(0,51,153)" v-on:click="install">
            <v-icon>mdi-palette</v-icon>
            <translate>Install</translate>
          </v-btn>
          <v-btn text color="rgb(0,51,153)" v-on:click="close">
            <translate>Cancel</translate>
          </v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
    <v-card v-if="step == 'done'" class="mx-auto my-3 pa-1" elevation=8 max-width="500px">
      <v-card-title>
        <translate>
          Installation Completed
        </translate>
      </v-card-title>
      <v-card-text>
        <translate>
          Inkscape palettes have been installed. Please restart Inkscape to load the new palettes.
        </translate>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="rgb(0,51,153)" v-on:click="close">
          Done
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card v-if="step == 'error'" class="mx-auto my-3 pa-1" elevation=8 max-width="500px">
      <v-card-title>
        <translate>
          Installation Failed
        </translate>
      </v-card-title>
      <v-card-text>
        <translate>Inkscape add-on installation failed</translate>
      </v-card-text>
      <v-card-text class="text--secondary">
        {{ error }}
      </v-card-text>
      <v-card-actions>
        <v-btn text color="rgb(0,51,153)" v-on:click="retry">
          <translate>Try again</translate>
        </v-btn>
        <v-btn text color="rgb(0,51,153)" v-on:click="close">
          <translate>Cancel</translate>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
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
