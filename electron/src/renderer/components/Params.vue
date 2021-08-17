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
      <v-col cols="12">
        <v-card class="pa-0 ma-2">
          <v-tabs v-model="tab" :hide-slider="hide_slider" v-on:change="hide_slider = false" class="main-tabs" vertical
                  background-color="grey lighten-5" optional>
            <v-tab v-if="num_nodes.running_stitch" key="running-stitch" v-on:change="selected = ['running_stitch']">
              <img class="tab-icon" :src="require('../assets/icons/running_stitch.png')" width="20px" height="20px"/>
              <translate>Running Stitch</translate>
            </v-tab>
            <v-tab v-if="num_nodes.satin_stitch" key="satin" v-on:change="selected = ['satin_stitch']">
              <img class="tab-icon" :src="require('../assets/icons/satin_stitch.png')" width="20px" height="20px"/>
              <translate>Satin</translate>
            </v-tab>
            <v-tab v-if="num_nodes.fill_stitch" key="fill-stitch" v-on:change="selected = ['fill_stitch']">
              <img class="tab-icon" :src="require('../assets/icons/fill_stitch.png')" width="20px" height="20px"/>
              <translate>Fill Stitch</translate>
            </v-tab>
            <v-tab v-if="num_nodes.polyline" key="polyline" v-on:change="selected = ['polyline']">
              <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
              <translate>Polyline</translate>
            </v-tab>
            <v-tab v-if="num_nodes.clone" key="clone" v-on:change="selected = ['clone']">
              <img class="tab-icon" :src="require('../assets/icons/clone.png')" width="20px" height="20px"/>
              <translate>Clone</translate>
            </v-tab>
            <v-tab v-if="num_nodes.manual_stitch" key="manual_stitch"
                   v-on:change="selected = ['running_stitch', 'satin_stitch', 'manual_stitch', 'polyline']">
              <img class="tab-icon" :src="require('../assets/icons/manual_stitch.png')" width="20px" height="20px"/>
              <translate>Manual Stitch</translate>
            </v-tab>
            <v-tab key="helper" disabled>
            </v-tab>

            <v-tab-item v-if="num_nodes.running_stitch" key="running_stitch">
              <running-stitch-tab/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.satin_stitch" key="satin">
              <satin-tab/>
            </v-tab-item>
            <v-tab-item v-if=" num_nodes.fill_stitch">
              <fill-stitch-tab/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.polyline" key="polyline">
              <polyline-tab/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.clone" key="clone">
              <clone-tab/>
            </v-tab-item>
            <v-tab-item v-if="num_nodes.manual_stitch" key="manual_stitch">
              <manual-stitch-tab/>
            </v-tab-item>
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
          </v-tabs>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
const inkStitch = require("../../lib/api")
import ParamsThumbnail from './ParamsThumbnail.vue'
import RunningStitchTab from './RunningStitchTab.vue'
import SatinTab from './SatinTab.vue'
import FillStitchTab from './FillStitchTab.vue'
import PolylineTab from './PolylineTab.vue'
import CloneTab from './CloneTab.vue'

export default {
  name: "Params",
  components: {
    ParamsThumbnail,
    RunningStitchTab,
    SatinTab,
    FillStitchTab,
    PolylineTab,
    CloneTab,
  },
  data: function () {
    return {
      nodes: [],
      num_nodes: new Object(),
      selected: [],
      tab: null,
      hide_slider: true,
    }
  },
  computed: {
    thumbnail_url() {
      return `${inkStitch.url}/params/thumbnail/path4440-3-1-0`
    },
    logo() {
      return require("../assets/logo.png")
    }
  },
  created: function () {
    inkStitch.get('/params/objects').then(response => {
      this.nodes = response.data.nodes
      this.num_nodes = response.data.num_nodes
    })

    this.tab = 5
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

</style>
