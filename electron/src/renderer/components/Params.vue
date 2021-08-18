<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="12">
        <v-card class="pa-2 ma-2">
          <div class="node-list material-scrollbar py-2">
            <params-thumbnail v-for="node in nodes" :key="node.id" class="thumbnail" :selected="selected" v-bind="node"></params-thumbnail>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <v-card class="pa-0 ma-2">
          <v-tabs v-model="tab" class="main-tabs" vertical
                  background-color="grey lighten-5">
            <v-tab key="helper" style="display: none">
            </v-tab>
            <v-tab v-if="num_nodes.running_stitch" key="running-stitch" v-on:change="selected = 'running_stitch'">
              <img class="tab-icon" :src="require('../assets/icons/running_stitch.png')" width="20px" height="20px"/>
              <translate>Running Stitch</translate>
            </v-tab>
            <v-tab v-if="num_nodes.satin_stitch" key="satin-stitch" v-on:change="selected = 'satin_stitch'">
              <img class="tab-icon" :src="require('../assets/icons/satin_stitch.png')" width="20px" height="20px"/>
              <translate>Satin Stitch</translate>
            </v-tab>
            <v-tab v-if="num_nodes.fill_stitch" key="fill-stitch" v-on:change="selected = 'fill_stitch'">
              <img class="tab-icon" :src="require('../assets/icons/fill_stitch.png')" width="20px" height="20px"/>
              <translate>Fill Stitch</translate>
            </v-tab>
            <v-tab v-if="num_nodes.polyline" key="polyline" v-on:change="selected = 'polyline'">
              <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
              <translate>Polyline</translate>
            </v-tab>
            <v-tab v-if="num_nodes.clone" key="clone" v-on:change="selected = 'clone'">
              <img class="tab-icon" :src="require('../assets/icons/clone.png')" width="20px" height="20px"/>
              <translate>Clone</translate>
            </v-tab>
            <v-tab v-if="num_nodes.manual_stitch" key="manual_stitch" v-on:change="selected = 'manual_stitch'">
              <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
              <translate>Manual Stitch</translate>
            </v-tab>

            <v-tab-item>
              <v-card flat class="pl-12 pt-8">
                <v-card-text class="text-h5 pa-0">
                  <font-awesome-icon icon="arrow-left" style="vertical-align: middle"></font-awesome-icon>
                  <translate class="pl-2">
                    select an option
                  </translate>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.running_stitch" key="running_stitch">
              <running-stitch-tab ref="runningStitchTab" class="params-tab"/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.satin_stitch" key="satin_stitch">
              <satin-stitch-tab ref="satinStitchTab" v-on:enable-manual-stitch="enable_manual_stitch" class="params-tab"/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.fill_stitch">
              <fill-stitch-tab ref="fillStitchTab" class="params-tab"/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.polyline" key="polyline">
              <polyline-tab ref="polylineTab" class="params-tab"/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.clone" key="clone">
              <clone-tab ref="cloneTab" class="params-tab"/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.manual_stitch" key="manual_stitch">
              <manual-stitch-tab ref="manualStitchTab" v-on:disable-manual-stitch="disable_manual_stitch" class="params-tab"/>
            </v-tab-item>
          </v-tabs>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <presets-panel class="pa-0 ma-2"></presets-panel>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <v-card flat class="pa-0 ma-2">
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
</template>

<script>
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
    ManualStitchTab
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

.params-tab {
  overflow-y: auto;
  max-height: 50vh;
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

</style>
