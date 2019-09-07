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
  faFrog,
  faHippo,
  faHorse,
  faInfo,
  faMinus,
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
  faFrog,
  faHippo,
  faHorse,
  faInfo,
  faMinus,
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

Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  components: {App},
  router,
  template: '<App/>'
}).$mount('#app')
