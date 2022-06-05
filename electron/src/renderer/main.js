/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

// ES6
import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'

import {library} from '@fortawesome/fontawesome-svg-core'
import {
  faAlignRight,
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faAngleRight,
  faCircle,
  faCut,
  faExchangeAlt,
  faEye,
  faFrog,
  faLink,
  faHippo,
  faHorse,
  faInfo,
  faMinus,
  faPalette,
  faPause,
  faPlay,
  faPlus,
  faShoePrints,
  faSpinner,
  faStepBackward,
  faStepForward,
  faStop
} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon, FontAwesomeLayers} from '@fortawesome/vue-fontawesome'
import Transitions from 'vue2-transitions'
import GetTextPlugin from 'vue-gettext'
import translations from './assets/translations.json'
import {selectLanguage} from '../lib/i18n'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

// We have to add to the library every icon we use anywhere in the UI.
// This avoids the need to bundle the entire font-awesome icon set with
// Ink/Stitch.
library.add(
  faAlignRight,
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faAngleRight,
  faCircle,
  faCut,
  faExchangeAlt,
  faEye,
  faFrog,
  faLink,
  faHippo,
  faHorse,
  faInfo,
  faMinus,
  faPalette,
  faPause,
  faPlay,
  faPlus,
  faShoePrints,
  faSpinner,
  faStepBackward,
  faStepForward,
  faStop
)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('font-awesome-layers', FontAwesomeLayers)

Vue.use(Transitions)
Vue.use(GetTextPlugin, {
  translations: translations,
  defaultLanguage: selectLanguage(translations),
  silent: true
})

Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

Vue.use(Vuetify)
const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#003399',
        secondary: '#000000',
        accent: '#8c9eff',
        error: '#b71c1c',
      },
    },
  },
})

/* eslint-disable no-new */
new Vue({
  vuetify,
  components: {App},
  router,
  template: '<App/>'
}).$mount('#app')
