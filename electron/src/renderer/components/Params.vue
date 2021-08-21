<template>
  <multipane layout="vertical" style="min-width: 100vw;">
    <div style="min-width: 30vw;">
      <v-container class="grow d-flex flex-column flex-nowrap container" style="min-height: 100vh; max-height: 100vh;">
        <v-row class="shrink">
          <v-col cols="12">
            <v-card class="pa-2">
              <div class="node-list material-scrollbar py-2">
                <params-thumbnail v-for="node in nodes" :key="node.id" class="thumbnail" :selected="selected" v-bind="node"></params-thumbnail>
              </div>
            </v-card>
          </v-col>
        </v-row>
        <v-row class="grow">
          <v-col cols="12">
            <v-card class="pa-0 fill-height">
              <v-tabs v-model="tab" class="main-tabs fill-height" vertical
                      background-color="grey lighten-5">
                <v-tab key="helper" style="display: none">
                </v-tab>
                <v-tab v-if="num_nodes.running_stitch" key="running-stitch" v-on:change="selected = 'running_stitch'">
                  <img class="tab-icon" :src="require('../assets/icons/running_stitch.png')" width="20px" height="20px"/>
                  <translate>Running Stitch</translate> &nbsp; ({{ num_nodes.running_stitch }})
                </v-tab>
                <v-tab v-if="num_nodes.satin_stitch" key="satin-stitch" v-on:change="selected = 'satin_stitch'">
                  <img class="tab-icon" :src="require('../assets/icons/satin_stitch.png')" width="20px" height="20px"/>
                  <translate>Satin Stitch</translate> &nbsp; ({{ num_nodes.satin_stitch }})
                </v-tab>
                <v-tab v-if="num_nodes.fill_stitch" key="fill-stitch" v-on:change="selected = 'fill_stitch'">
                  <img class="tab-icon" :src="require('../assets/icons/fill_stitch.png')" width="20px" height="20px"/>
                  <translate>Fill Stitch</translate> &nbsp; ({{ num_nodes.fill_stitch }})
                </v-tab>
                <v-tab v-if="num_nodes.polyline" key="polyline" v-on:change="selected = 'polyline'">
                  <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
                  <translate>Polyline</translate> &nbsp; ({{ num_nodes.running_stitch }})
                </v-tab>
                <v-tab v-if="num_nodes.clone" key="clone" v-on:change="selected = 'clone'">
                  <img class="tab-icon" :src="require('../assets/icons/clone.png')" width="20px" height="20px"/>
                  <translate>Clone</translate> &nbsp; ({{ num_nodes.clone }})
                </v-tab>
                <v-tab v-if="num_nodes.manual_stitch" key="manual_stitch" v-on:change="selected = 'manual_stitch'">
                  <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
                  <translate>Manual Stitch</translate> &nbsp; ({{ num_nodes.manual_stitch }})
                </v-tab>

                <v-tab-item>
                  <v-card flat class="pl-12 pt-8 fill-height" disabled>
                    <v-card-text class="text-h5 pa-0">
                      <font-awesome-icon icon="arrow-left" style="vertical-align: middle"></font-awesome-icon>
                      <translate class="pl-2">
                        select a tab
                      </translate>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.running_stitch" key="running_stitch">
                  <running-stitch-tab ref="runningStitchTab" v-on:enable-manual-stitch="enable_manual_stitch" class="params-tab material-scrollbar"/>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.satin_stitch" key="satin_stitch">
                  <satin-stitch-tab ref="satinStitchTab" v-on:enable-manual-stitch="enable_manual_stitch" class="params-tab material-scrollbar"/>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.fill_stitch">
                  <fill-stitch-tab ref="fillStitchTab" class="params-tab material-scrollbar"/>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.polyline" key="polyline">
                  <polyline-tab ref="polylineTab" class="params-tab material-scrollbar"/>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.clone" key="clone">
                  <clone-tab ref="cloneTab" class="params-tab material-scrollbar"/>
                </v-tab-item>
                <v-tab-item v-if="num_nodes.manual_stitch" key="manual_stitch">
                  <manual-stitch-tab ref="manualStitchTab" v-on:disable-manual-stitch="disable_manual_stitch" class="params-tab material-scrollbar"/>
                </v-tab-item>
              </v-tabs>
            </v-card>
          </v-col>
        </v-row>
        <v-row class="shrink">
          <v-col cols="12">
            <presets-panel class="pa-0"></presets-panel>
          </v-col>
        </v-row>
        <v-row class="shrink">
          <v-col cols="12">
            <v-card flat class="pa-0">
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-on:click="apply" text color="primary">
                  <translate>Apply and Quit</translate>
                </v-btn>
                <v-btn v-on:click="cancel" text color="primary">
                  <translate>Cancel</translate>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <multipane-resizer class="multipane-resizer"></multipane-resizer>
    <div class="grow py-6 mr-2" style="min-width: 30vh">
      <v-card class="fill-height pa-2">
        <v-card-title>
          Simulator goes here
        </v-card-title>
      </v-card>
    </div>
  </multipane>
</template>

<script>
import {Multipane, MultipaneResizer} from 'vue-multipane';

import PresetsPanel from './PresetsPanel.vue'
import ParamsThumbnail from './ParamsThumbnail.vue'
import RunningStitchTab from './RunningStitchTab.vue'
import SatinStitchTab from './SatinStitchTab.vue'
import FillStitchTab from './FillStitchTab.vue'
import PolylineTab from './PolylineTab.vue'
import CloneTab from './CloneTab.vue'
import ManualStitchTab from './ManualStitchTab.vue'

const inkStitch = require('../../lib/api')

export default {
  name: 'Params',
  components: {
    PresetsPanel,
    ParamsThumbnail,
    RunningStitchTab,
    SatinStitchTab,
    FillStitchTab,
    PolylineTab,
    CloneTab,
    ManualStitchTab,
    Multipane,
    MultipaneResizer
  },
  data: function () {
    return {
      nodes: [],
      num_nodes: {},
      selected: null,
      tab: null,
      preset: null
    }
  },
  computed: {
    thumbnail_url() {
      return `${inkStitch.url}/params/thumbnail/path4440-3-1-0`
    },
    logo() {
      return require('../assets/logo.png')
    },
    presets() {
      return ["hello", "world"]
    }
  },
  methods: {
    enable_manual_stitch() {
      /*
         Manual stitch is special.  When we change this setting, a different
         Element class is used on the Python side.  That means we need to
         reload all objects and re-render the UI.

         This is the only case where a setting is applied immediately.
       */
      this.nodes = []
      this.num_nodes = []
      inkStitch.post('/params/manual_stitch/enable').then(response => {
        this.update_objects()
      })
    },
    disable_manual_stitch() {
      this.nodes = []
      this.num_nodes = []
      inkStitch.post('/params/manual_stitch/disable').then(response => {
        this.update_objects()
      })
    },
    update_objects() {
      inkStitch.get('/params/objects').then(response => {
        this.nodes = response.data.nodes
        this.num_nodes = response.data.num_nodes
        this.tab = 0
      })
    },
    apply() {
      Object.values(this.$refs).forEach(tab => {
        tab.apply()
      })
    },
    cancel() {

    }
  },
  created: function () {
    this.update_objects()
  }
}
</script>

<style scoped>
.thumbnail {
  display: inline-block;
}

.node-list {
  overflow-x: scroll;
  white-space: nowrap;
}

.node-list div.v-card {
  vertical-align: top;
  display: inline-block;
}

.material-scrollbar::-webkit-scrollbar {
  height: 10px;
  width: 10px;
  background-color: transparent;
}

.material-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, .3);
  background-color: rgb(140, 168, 224);
}

.tab-icon {
  margin-right: 10px;
}

.main-tabs .v-tab {
  justify-content: left;
}

/* These next two make it so that the params tab takes up all available height but doesn't cause
   the whole page to scroll.  It gets a scrollbar when it has more content than will fit.
 */
.params-tab {
  overflow-y: scroll;

  /* I don't really understand this.  I found it on stack overflow.  Somehow this
     works when max-height: 100% doesn't.
   */
  position: absolute;
  top: 8px;
  bottom: 8px;
  left: 8px;
  right: 8px;
}

.main-tabs::v-deep .v-window__container {
  height: 100% !important;
}

.multipane-resizer {
  height: 100vh;
  margin: 0;
  left: 0;
  position: relative;
}

.multipane-resizer:before {
  display: block;
  content: "";
  width: 5px;
  height: 200px;
  position: absolute;
  top: calc(50% + 100px);
  left: -1.25px;
  margin-top: -200px;
  margin-left: -2.5px;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
}

.multipane-resizer:before:hover {
  border-color: #999;
}

</style>
