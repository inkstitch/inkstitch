<template>
  <div>
    <font-awesome-icon icon="palette" class="info-icon"/>
    <p>
      <translate>Ink/Stitch can install palettes for Inkscape matching the thread colors from popular machine embroidery thread manufacturers.
      </translate>
    </p>
    <p>
      <translate>Choose Inkscape directory</translate>
      <input v-bind:value="path"/>
    </p>
    <button v-on:click="install">
      <translate>Install</translate>
    </button>
    <button v-on:click="cancel">
      <translate>Cancel</translate>
    </button>
  </div>
</template>

<script>
const inkStitch = require("../../lib/api")

export default {
  name: "InstallPalettes",
  data: function () {
    return {
      path: "",
    }
  },
  methods: {
    install() {
      alert("install button clicked")
    },
    cancel() {
      alert("cancel button clicked")
    }
  },
  created: function () {
    inkStitch.get("/install/default-path").then(response => {
      this.path = response.data
    })
  }
}
</script>

<style scoped>

</style>
