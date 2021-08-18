<template>
  <v-card class="pa-1 pt-2 mx-1" :disabled="!is_selected" :color="is_selected ? 'white' : 'grey lighten-3'">
    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-card-title class="py-0 px-1 my-1 text-subtitle-2 text-truncate d-block allow-hover"
                      style="max-width: 100px"
                      v-text="name"
                      v-on="on"
                      v-bind="attrs"
                      :disabled="false"></v-card-title>
      </template>
      <span>{{ name }}</span>
    </v-tooltip>
    <v-img ref="thumbnail" class="checkerboard allow-hover align-end" contain :src="thumbnail_url" width="100px" height="100px">
    </v-img>
    <v-card-actions class="pa-0">
      <v-tooltip bottom v-if="running_stitch">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Running Stitch')"
                 :src="require('../assets/icons/running_stitch.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Running Stitch</translate></span>
      </v-tooltip>
      <v-tooltip bottom v-if="satin_stitch" :disabled="false">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Satin Stitch')"
                 :src="require('../assets/icons/satin_stitch.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Satin Stitch</translate></span>
      </v-tooltip>
      <v-tooltip bottom v-if="fill_stitch" :disabled="false">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Fill Stitch')"
                 :src="require('../assets/icons/fill_stitch.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Fill Stitch</translate></span>
      </v-tooltip>
      <v-tooltip bottom v-if="clone" :disabled="false">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Clone')"
                 :src="require('../assets/icons/clone.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Clone</translate></span>
      </v-tooltip>
      <v-tooltip bottom v-if="polyline" :disabled="false">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Polyline')"
                 :src="require('../assets/icons/manual_stitch.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Polyline</translate></span>
      </v-tooltip>
      <v-tooltip bottom v-if="manual_stitch" :disabled="false">
        <template v-slot:activator="{on, attrs}">
          <v-img class="icon ml-1 my-1 allow-hover"
                 :alt="$gettext('Manual Stitch')"
                 :src="require('../assets/icons/manual_stitch.png')"
                 v-on="on"
                 v-bind="attrs"
                 max-width="20px"></v-img>
        </template>
        <span><translate>Manual Stitch</translate></span>
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script>
const inkStitch = require('../../lib/api')

export default {
  name: 'ParamsThumbnail',
  props: {
    node_id: String,
    name: String,
    selected: String
  },
  data: function () {
    return {
      running_stitch: null,
      satin_stitch: null,
      fill_stitch: null,
      manual_stitch: null,
      polyline: null,
      clone: null,
      visible: false
    }
  },
  computed: {
    thumbnail_url() {
      if (this.visible) {
        return `${inkStitch.url}/params/thumbnail/${this.node_id}`
      } else {
        return ''
      }
    },
    is_selected() {
      return this[this.selected]
    }
  },
  created: function () {
    inkStitch.get(`params/object-types/${this.node_id}`).then(response => {
      Object.assign(this, response.data)
    })
  },
  mounted() {
    // This stuff makes it so that the thumbnail isn't generated until they've
    // scrolled it into view.  That way, if they select a bunch of stuff, we
    // don't kill their CPU by generating all the thumbnails at once.
    this.observer = new IntersectionObserver(entries => {
      const image = entries[0];
      if (image.isIntersecting) {
        this.visible = true;
        this.observer.disconnect();
      }
    }, {root: this.$parent.$el});

    this.observer.observe(this.$refs.thumbnail.$el);
  },
}
</script>

<style scoped>
.icon {
  display: inline-block;
}

.checkerboard:hover {
  /* this magic is from https://stackoverflow.com/a/51054396 */
  background-image: linear-gradient(to right, rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)),
  linear-gradient(to right, black 50%, white 50%),
  linear-gradient(to bottom, black 50%, white 50%);
  background-blend-mode: normal, difference, normal;
  background-size: 8px 8px;
  background-repeat: repeat;
}

.allow-hover {
  pointer-events: auto;
  user-select: auto;
  cursor: default;
}
</style>
