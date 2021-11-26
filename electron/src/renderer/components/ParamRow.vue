<template>
  <tr>
    <td>
      <v-tooltip right>
        <template v-slot:activator="{on, attrs}">
          <v-btn text v-on:click="force_changed" v-on="on"
                 v-bind="attrs">
            <v-img v-if="changed"
                   :alt="$gettext('pencil icon')"
                   :src="require('../assets/icons/pencil.png')"
                   max-width="20px"></v-img>
          </v-btn>
        </template>
        <translate v-if="changed" key="is_changed">This parameter will be saved when you click "Apply and Quit"</translate>
        <translate v-else key="is_not_changed">Click to force this parameter to be saved when you click "Apply and Quit"</translate>
      </v-tooltip>
    </td>
    <td>
      <v-tooltip bottom>
        <template v-slot:activator="{on, attrs}">
          <label :for="param_id" v-on="on" v-bind="attrs">
            <slot></slot>
          </label>
        </template>
        <slot name="tooltip">
          <!-- If no tooltip slot was provided, we just show the label as the tooltip.
               Not ideal, but I'm not sure how to prevent the tooltip in this case. -->
          <slot></slot>
        </slot>
      </v-tooltip>
    </td>
    <td class="param-cell">
      <v-checkbox :id="param_id" :ripple="false" v-if="type === 'checkbox'" v-model="valueModel" hide-details></v-checkbox>
      <v-text-field :id="param_id" v-if="type === 'text'" v-model="valueModel" hide-details></v-text-field>
      <v-select :id="param_id" :items="items" v-if="type === 'select'" v-model="valueModel" hide-details></v-select>
    </td>
    <td class="unit">{{ unit }}</td>
  </tr>

</template>

<script>
var param_id = 0

export default {
  name: "ParamRow",
  props: {
    "value": [String, Boolean, Number],
    "label": String,
    "unit": String,
    "type": {
      type: String,
      default: 'text'
    },
    "changed": Boolean,
    "items": Array
  },
  computed: {
    /* We need a level of indirection here because we're not supposed to modify a prop.
       Passing a prop directly as a v-model would modify it.
     */
    valueModel: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('update:value', value)
      }
    }
  },
  methods: {
    force_changed() {
      this.$emit('update:changed', true)
    }
  },
  beforeCreate() {
    this.param_id = `param-${param_id.toString()}`
    param_id += 1
  }
}
</script>

<style scoped>

.param-cell::v-deep .v-input__control {
  max-width: 100px !important;
}

td {
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 2px;
  padding-bottom: 2px;
}

td.unit {
  text-align: left;
  vertical-align: bottom;
  padding-left: 2px;
}

.v-input {
  margin-top: 0px;
  padding-top: 0px;
}

tr:hover {
  background-color: rgb(229, 238, 255);
}

</style>
