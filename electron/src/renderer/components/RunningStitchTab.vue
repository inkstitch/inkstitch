<template>
  <v-card flat>
    <v-simple-table>
      <tbody>
      <tr>
        <td></td>
        <td>
          <translate>Manual stitch placement</translate>
        </td>
        <td>
          <v-checkbox v-model="manual_stitch_placement"></v-checkbox>
        </td>
        <td></td>
      </tr>
      <tr>
        <td></td>
        <td>
          <translate>Manual stitch placement</translate>
        </td>
        <td>
          <v-combobox v-model="thing" :items="['thing1', 'thing2']"></v-combobox>
        </td>
        <td></td>
      </tr>
      </tbody>
    </v-simple-table>
  </v-card>
</template>

<script>
import {ParamsTabMixin} from '../../lib/mixins'

export default {
  name: 'RunningStitchTab',
  mixins: [ParamsTabMixin],
  data: function () {
    return {
      manual_stitch_placement: null,
      thing: null
    }
  }
}
</script>

<style scoped>

</style>
