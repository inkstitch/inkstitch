<template>
  <v-card>
    <v-card-actions>
      <v-combobox solo
                  :items="presets"
                  v-model="preset"
                  class="ma-1 mr-8"
                  persistent-hint
                  :hint="$gettext('Select a preset or enter a new preset name')"></v-combobox>
      <v-btn v-on:click="load_preset" text color="primary">
        <translate>Load</translate>
      </v-btn>
      <v-btn v-on:click="add_preset" text color="primary">
        <translate>Add</translate>
      </v-btn>
      <v-btn v-on:click="overwrite_preset" text color="primary">
        <translate>Overwrite</translate>
      </v-btn>
      <v-btn v-on:click="delete_preset" text color="primary">
        <translate>Delete</translate>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "PresetsPanel.vue",
  data: function () {
    return {
      presets: ["preset 1", "preset 2", "other thing"],
      preset: null
    }
  },
  methods: {
    load_preset() {
    },
    add_preset() {
    },
    overwrite_preset() {
    },
    delete_preset() {
    },
  }
}
</script>

<style scoped>

</style>
