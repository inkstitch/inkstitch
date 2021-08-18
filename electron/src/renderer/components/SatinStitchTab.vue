<template>
  <v-card flat>
    <v-card-title>Satin Stitch</v-card-title>
    <v-card-text>
      <v-checkbox v-on:change="$emit('enable-manual-stitch')" :label="$gettext('manual stitch mode')" hide-details></v-checkbox>
      <v-radio-group v-model="params.satin_column" row hide-details>
        <v-radio :label="$gettext('satin column')" :value="true"></v-radio>
        <v-radio :label="$gettext('basic satin')" :value="false"></v-radio>
      </v-radio-group>
      <v-card flat v-if="params.satin_column">
        <v-card-text class="pt-0">
          <v-checkbox v-model="params.setting1" :label="$gettext('setting1')" hide-details></v-checkbox>
        </v-card-text>
      </v-card>
      <v-card flat v-if="params.satin_column === false">
        <v-card-text class="pt-0">
          <v-checkbox v-model="params.setting2" :label="$gettext('setting2')" hide-details></v-checkbox>
        </v-card-text>
      </v-card>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>
      this is a test<br/>


    </v-card-text>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../../lib/mixins'

export default {
  name: 'SatinStitchTab',
  element_type: 'satin_stitch',
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      params: {
        satin_column: null,
        setting1: false,
        setting2: false
      }
    }
  }
}
</script>

<style scoped>

</style>
