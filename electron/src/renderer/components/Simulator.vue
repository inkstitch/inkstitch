<template>
  <div ref = "simulator" class="simulator vld-parent">
    <div class="panel">
      <fieldset class="controls">
        <legend>Controls</legend>
        <button v-on:click="stop" :class="{pressed: paused}"><font-awesome-icon icon="pause" size="2x" class="fa-button" /></button>
        <button v-on:click="start" :class="{pressed: animating}"><font-awesome-icon icon="play" size="2x" class="fa-button" /></button>
        <button v-on:click="animationReverse" :class="{pressed: reverse}"><font-awesome-icon icon="angle-double-left" size="2x" class="fa-button" :mask="['fas', 'stop']" /></button>
        <button v-on:click="animationForward" :class="{pressed: forward}"><font-awesome-icon icon="angle-double-right" size="2x" class="fa-button" :mask="['fas', 'stop']" /></button>
        <button v-on:click="animationBackwardOneStitch"><font-awesome-icon icon="step-backward" size="2x" class="fa-button" /></button>
        <button v-on:click="animationForwardOneStitch"><font-awesome-icon icon="step-forward" size="2x" class="fa-button" /></button>        
      </fieldset>
      <fieldset class="speed">
        <legend>Speed: {{speed}} stitches/sec</legend>
        <button v-on:click="animationSlowDown"><font-awesome-icon icon="angle-right" size="2x" class="fa-button" /></button>
        <button v-on:click="animationSpeedUp"><font-awesome-icon icon="angle-double-right" size="2x" class="fa-button" /></button>
      </fieldset>
      <fieldset class="command">
        <legend>Command</legend>
        <span>{{currentCommand}}</span>
      </fieldset>
    </div>
    <div class="slider-container">
      <span>1</span>
      <span class="slider-box">
        <vue-slider
                  :value="currentStitchDisplay"
                  @change="setCurrentStitch"
                  :min="1"
                  :max="numStitches"
                  :duration="0"></vue-slider>
      </span>
      <span>{{numStitches}}</span>
      <input ref="currentStitchInput"
           class="current-stitch-input"
           :value="currentStitchDisplay"
           @change="onCurrentStitchEntered"
           @focus="stop" />
    </div>
    <loading :active.sync="loading" :is-full-page="false">
      <div class="loading">
        <div class="loading-icon"><font-awesome-icon icon="spinner" size="4x" pulse /></div>
        <div class="loading-text">Rendering stitch-plan...</div>
      </div>
    </loading>
  </div>
</template>

<script>
  const inkStitch = require("../../lib/api")
  const Mousetrap = require("mousetrap")
  const SVG = require("svg.js")
  require("svg.panzoom.js")
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  import VueSlider from 'vue-slider-component'
  import 'vue-slider-component/theme/default.css'
  const throttle = require('lodash.throttle')

  export default {
    name: 'simulator',
    components: {
      Loading,
      VueSlider
    },
    data: function() {
      return {
        loading: false,
        speed: 16,
        currentStitch: 1,
        currentStitchDisplay: 1,
        direction: 1,
        numStitches: 1,
        animating: false
      }
    },
    watch: {
      currentStitch: throttle(function() {
        this.currentStitchDisplay = this.currentStitch.toFixed()
      }, 100, {leading: true, trailing: true}),
    },
    computed: {
      speedDisplay() {
        return this.speed * this.direction
      },
      currentCommand() {
        let stitch = this.stitches[this.currentStitch.toFixed()]

        if (stitch === undefined) {
          return "NONE"
        }

        let label = "STITCH"
        switch(true) {
          case stitch.jump:
            label = "JUMP"
            break
          case stitch.trim:
            label = "TRIM"
            break
          case stitch.stop:
            label = "STOP"
            break
          case stitch.color_change:
            label = "COLOR CHANGE"
            break
        }

        return label
      },
      paused() {
        return !this.animating
      },
      forward() {
        return this.direction > 0
      },
      reverse() {
        return this.direction < 0
      },
    },
    methods: {
      animationSpeedUp() {
        this.speed *= 2.0
      },
      animationSlowDown() {
        this.speed = Math.max(this.speed/2.0, 1)
      },
      animationReverse() {
        this.direction = -1
        this.start()
      },
      animationForward() {
        this.direction = 1
        this.start()
      },
      toggleAnimation(e) {
        if (this.animating) {
          this.stop()
        } else {
          this.start()
        }

        e.preventDefault();
      },
      animationForwardOneStitch() {
        this.setCurrentStitch(this.currentStitch + 1)
      },
      animationBackwardOneStitch() {
        this.setCurrentStitch(this.currentStitch - 1)
      },
      onCurrentStitchEntered() {
        let newCurrentStitch = parseInt(this.$refs.currentStitchInput.value)

        if (isNaN(newCurrentStitch)) {
          this.$refs.currentStitchInput.value = this.currentStitch.toFixed()
        } else {
          this.setCurrentStitch(parseInt(newCurrentStitch))
        }
      },
      setCurrentStitch(newCurrentStitch) {
        this.stop()
        this.currentStitch = newCurrentStitch
        this.clampCurrentStitch()
        this.renderFrame()
      },
      clampCurrentStitch() {
        this.currentStitch = Math.max(Math.min(this.currentStitch, this.numStitches), 1)
      },
      animate() {
        let frameStart = performance.now()
        let frameTime = null

        if (this.lastFrameStart !== null) {
          frameTime = frameStart - this.lastFrameStart
        } else {
          frameTime = this.targetFramePeriod
        }

        this.lastFrameStart = frameStart

        let numStitches = this.speed * Math.max(frameTime, this.targetFramePeriod) / 1000.0;
        this.currentStitch = this.currentStitch + numStitches * this.direction
        this.clampCurrentStitch()

        this.renderFrame()

        if (this.animating && this.shouldAnimate()) {
          this.timer = setTimeout(this.animate, Math.max(0, this.targetFramePeriod - frameTime))
        } else {
          this.timer = null;
          this.stop()
        }
      },
      renderFrame() {
        while (this.renderedStitch < this.currentStitch) {
          this.renderedStitch += 1
          this.stitchPaths[this.renderedStitch].show();
        }

        while (this.renderedStitch >= this.currentStitch) {
          this.stitchPaths[this.renderedStitch].hide();
          this.renderedStitch -= 1
        }
      },
      shouldAnimate() {
        if (this.direction == 1 && this.currentStitch < this.numStitches) {
          return true;
        } else if (this.direction == -1 && this.currentStitch > 1) {
          return true;
        } else {
          return false;
        }
      },
      start() {
        if (!this.animating && this.shouldAnimate()) {
          this.animating = true
          this.timer = setTimeout(this.animate, 0);
        }
      },
      stop() {
        if (this.animating) {
          if (this.timer) {
            clearTimeout(this.timer)
            this.timer = null
          }
          this.animating = false
          this.lastFrameStart = null
        }
      }
    },
    created: function() {
      // non-reactive properties
      this.targetFPS = 30
      this.targetFramePeriod = 1000.0 / this.targetFPS,
      this.renderedStitch = 0
      this.lastFrameStart = null
      this.stitchPaths = [null]  // 1-indexed to match up with stitch number display
      this.stitches = [null]
      this.svg = null
      this.simulation = null
      this.timer = null
    },
	  mounted: function() {
      this.svg = SVG(this.$refs.simulator).panZoom({zoomMin: 0.1})
      this.svg.node.style.flex_grow = 1
      this.svg.node.style.flex_shrink = 1
      this.svg.node.style.order = -1
            
      this.simulation = this.svg.group()

      this.loading = true

      inkStitch.get('stitch_plan').then(response => {
        var stitch_plan = response.data
          let [minx, miny, maxx, maxy] = stitch_plan.bounding_box    
          let width = maxx - minx
          let height = maxy - miny    
          this.svg.viewbox(0, 0, width, height);
        
        stitch_plan.color_blocks.forEach(color_block => {
          let attrs = {fill: "none", stroke: `${color_block.color.visible_on_white.hex}`, "stroke-width": 0.3}
          let stitching = false
          let prevStitch = null
          color_block.stitches.forEach(stitch => {
            stitch.x -= minx
            stitch.y -= miny

            if (stitching && prevStitch) {
              this.stitchPaths.push(this.simulation.path(`M${prevStitch.x},${prevStitch.y} ${stitch.x},${stitch.y}`).attr(attrs).hide())
            } else {
              this.stitchPaths.push(this.simulation.path(`M${stitch.x},${stitch.y} ${stitch.x},${stitch.y}`).attr(attrs).hide())
            }
            this.stitches.push(stitch)

            if (stitch.trim || stitch.color_change) {
              stitching = false
            } else if (!stitch.jump) {
              stitching = true
            }

            prevStitch = stitch
          })
        })

        this.loading = false

        this.numStitches = this.stitches.length - 1

        // v-on:keydown doesn't seem to work, maybe an Electron issue?
        Mousetrap.bind("up", this.animationSpeedUp)
        Mousetrap.bind("down", this.animationSlowDown)
        Mousetrap.bind("left", this.animationReverse)
        Mousetrap.bind("right", this.animationForward)
        Mousetrap.bind("space", this.toggleAnimation)
        Mousetrap.bind("+", this.animationForwardOneStitch)
        Mousetrap.bind("-", this.animationBackwardOneStitch)

        this.start()
      })
  	}
  }
</script>

<style scoped>
  .loading-icon {
    text-align: center;
    margin-bottom: 1rem;
    color: rgb(0, 51, 153);
  }

  .loading-text {
    font-family: sans-serif;
  }

  .loading {
    border-radius: 1rem;
    border: 3px solid rgb(0, 51, 153);
    background-color: rgba(0, 51, 153, 0.1);
    padding: 1rem;
  }

  .slider-container {
    margin-top: 10px;
    height: 25px;
  }

  .slider-container > * {
    display: inline-block;
    vertical-align: middle;
  }

  .slider-box {
    width: calc(80%);
    margin-left: 10px;
    margin-right: 10px;
  }

  .current-stitch-input {
    width: 4rem;
    float: right;
    font-size: 1rem;
  }

  .fa-spin-fast {
    animation: fa-spin 0.4s infinite linear;
  }

  .fa-button {
    margin: 3px;
  }

  .panel > * {
    display: inline-block;
    vertical-align: middle;
    text-align: center;
  }

  fieldset {
    text-align: center;
    height: 50px;
  }
  fieldset button {
    display: inline-block;
  }
  fieldset.command span {
    font-family: sans-serif;
    font-size: 2rem;
    vertical-align: middle;
  }
  button.pressed {
    border-style: inset;
  }
  .simulation {
    margin: 1rem;
    flex-grow: 1;
    flex-shrink: 1;
    order: -1;
  }
  .panel {
    flex-grow: 0;
  }
  .slider-container {
    flex-grow: 0;
  }
  .simulator {
    display: flex;
    flex-direction: column;
    height: 98vh;
  }
</style>