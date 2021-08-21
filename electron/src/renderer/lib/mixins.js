/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

const inkStitch = require('../../lib/api')
import ParamsTable from '../components/ParamsTable.vue'
import ParamRow from '../components/ParamRow.vue'

const ParamsTabMixin = {
  element_type: null, // define this in the component, example: running_stitch
  components: {
    ParamsTable,
    ParamRow
  },
  data: function () {
    return {
      params: {},
      changed: {}
    }
  },
  mounted() {
    Object.keys(this.params).forEach(param => {
      this.$watch(`params.${param}`, function (oldVal, newVal) {
        this.changed[param] = true
      })
    })
  },
  methods: {
    changed_params() {
      var params = {}
      Object.keys(this.changed).forEach(param => {
        params[param] = this.params[param]
      })

      return params
    },
    apply() {
      console.log('applying', this.$options.element_type)
      inkStitch.post(`/params/apply/${this.$options.element_type}`, this.changed_params()).then(response => {
        console.log('apply', this.$options.element_type, response);
      })
    }
  }
}

export {ParamsTabMixin}
