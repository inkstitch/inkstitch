<template>
  <div ref="simulator" class="simulator vld-parent">
    <fieldset>
      <div class="panel">
        <fieldset class="controls">
          <legend>Controls</legend>
          <button v-on:click="stop" :class="{pressed: paused}" title="Pause (space)">
            <font-awesome-icon icon="pause" size="2x" class="fa-button"/>
          </button>
          <button v-on:click="start" :class="{pressed: animating}" title="Play (arrow left | arrow right)">
            <font-awesome-icon icon="play" size="2x" class="fa-button"/>
          </button>
          <button v-on:click="animationReverse" :class="{pressed: reverse}" title="Play backward (arrow left)">
            <font-awesome-icon icon="angle-double-left" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
          </button>
          <button v-on:click="animationForward" :class="{pressed: forward}" title="Play forward (arrow right)">
            <font-awesome-icon icon="angle-double-right" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
          </button>
          <button v-on:click="animationBackwardOneStitch" title="One step backward (-)">
            <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button fa-flip-horizontal"/>
          </button>
          <button v-on:click="animationForwardOneStitch" title="One step forward (+)">
            <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button"/>
          </button>
          <button v-on:click="animationPreviousCommand" title="Jump to previous command (?)">
            <font-awesome-icon icon="step-backward" size="2x" class="fa-button"/>
          </button>
          <button v-on:click="animationNextCommand" title="Jump to next command (?)">
            <font-awesome-icon icon="step-forward" size="2x" class="fa-button"/>
          </button>
        </fieldset>
        <fieldset class="speed">
          <legend>Speed: {{speed}} stitches/sec</legend>
          <button v-on:click="animationSlowDown" title="Slow down (arrow down)">
            <font-awesome-icon icon="hippo" size="2x" class="fa-button"/>
          </button>
          <button v-on:click="animationSpeedUp" title="Speed up (arrow up)">
            <font-awesome-icon icon="align-right" class="fa-motion-lines"/>
            <font-awesome-icon icon="horse" size="2x" class="fa-button fa-fast"/>
          </button>
        </fieldset>
        <fieldset class="command">
          <legend>Command</legend>
          <span class="current-command">{{currentCommand}}</span>
        </fieldset>
        <fieldset class="show-commands">
          <legend>Show Commands</legend>
          <span>
          <input id="trim-checkbox" type="checkbox" v-model="showTrims"/><label for="trim-checkbox">✂ trims</label>
          <br/>
          <input id="jump-checkbox" type="checkbox" v-model="showJumps"/><label for="jump-checkbox">↷ jumps</label>
        </span>
          <span>
          <input id="color-change-checkbox" type="checkbox" v-model="showColorChanges"/><label for="color-change-checkbox">⇄ color changes</label>
          <br/>
          <input id="stop-checkbox" type="checkbox" v-model="showStops"/><label for="stop-checkbox">⏸ stops</label>
        </span>
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
          :duration="0"
          :marks="sliderMarks"
          :process="sliderProcess"></vue-slider>
      </span>
        <span>{{numStitches}}</span>
        <input ref="currentStitchInput"
               class="current-stitch-input"
               :value="currentStitchDisplay"
               @change="onCurrentStitchEntered"
               @focus="stop"/>
      </div>
    </fieldset>
    <loading :active.sync="loading" :is-full-page="false">
      <div class="loading">
        <div class="loading-icon">
          <font-awesome-icon icon="spinner" size="4x" pulse/>
        </div>
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

  function SliderMark(label, labelStyle) {
    this.label = label
    this.labelStyle = labelStyle
  }

  export default {
    name: 'simulator',
    components: {
      Loading,
      VueSlider
    },
    data: function () {
      return {
        loading: false,
        speed: 16,
        currentStitch: 1,
        currentStitchDisplay: 1,
        direction: 1,
        numStitches: 1,
        animating: false,
        sliderProcess: dotPos => this.sliderColorSections,
        showTrims: false,
        showJumps: false,
        showColorChanges: false,
        showStops: false
      }
    },
    watch: {
      currentStitch: throttle(function () {
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
        switch (true) {
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
      sliderMarks() {
        var marks = {}

        if (this.showTrims)
          Object.assign(marks, this.trimMarks);

        if (this.showJumps)
          Object.assign(marks, this.jumpMarks);

        if (this.showColorChanges)
          Object.assign(marks, this.colorChangeMarks);

        if (this.showStops)
          Object.assign(marks, this.stopMarks);

        return marks
      }
    },
    methods: {
      animationSpeedUp() {
        this.speed *= 2.0
      },
      animationSlowDown() {
        this.speed = Math.max(this.speed / 2.0, 1)
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
      animationNextCommand() {
        let nextCommandIndex = this.getNextCommandIndex()
        if (nextCommandIndex === -1) {
          this.setCurrentStitch(this.stitches.length)
        } else {
          this.setCurrentStitch(this.commandList[nextCommandIndex])
        }
      },
      animationPreviousCommand() {
        let nextCommandIndex = this.getNextCommandIndex()
        let prevCommandIndex = 0
        if (nextCommandIndex === -1) {
          prevCommandIndex = this.commandList.length - 2
        } else {
          prevCommandIndex = nextCommandIndex - 2
        }
        let previousCommand = this.commandList[prevCommandIndex]
        if (previousCommand === undefined) {
          previousCommand = 1
        }
        this.setCurrentStitch(previousCommand)
      },
      getNextCommandIndex() {
        let currentStitch = this.currentStitchDisplay
        let nextCommand = this.commandList.findIndex(function (command) {
          return command > currentStitch
        })
        return nextCommand
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
      },
      generateMarks() {
        this.commandList = Array()
        for (let i = 1; i < this.stitches.length; i++) {
          if (this.stitches[i].trim) {
            this.trimMarks[i] = new SliderMark("✂", {transform: "translate(-50%, -5px)"})
            this.commandList.push(i)
          } else if (this.stitches[i].stop) {
            this.stopMarks[i] = new SliderMark("⏸", {transform: "translate(-50%, 10px)"})
            this.commandList.push(i)
          } else if (this.stitches[i].jump) {
            this.jumpMarks[i] = new SliderMark("↷", {transform: "translate(-50%, -50px)"})
            this.commandList.push(i)
          } else if (this.stitches[i].color_change) {
            this.colorChangeMarks[i] = new SliderMark("⇄", {transform: "translate(-50%, 10px)"})
            this.commandList.push(i)
          }
        }
      },
      generateColorSections() {
        var currentStitch = 0
        this.stitchPlan.color_blocks.forEach(color_block => {
          this.sliderColorSections.push([
            (currentStitch + 1) / this.numStitches * 100,
            (currentStitch + color_block.stitches.length) / this.numStitches * 100,
            {backgroundColor: color_block.color.visible_on_white.hex}
          ])
          currentStitch += color_block.stitches.length
        })
      }
    },
    created: function () {
      // non-reactive properties
      this.targetFPS = 30
      this.targetFramePeriod = 1000.0 / this.targetFPS
      this.renderedStitch = 0
      this.lastFrameStart = null
      this.stitchPaths = [null]  // 1-indexed to match up with stitch number display
      this.stitches = [null]
      this.svg = null
      this.simulation = null
      this.timer = null
      this.sliderColorSections = []
      this.trimMarks = {}
      this.stopMarks = {}
      this.colorChangeMarks = {}
      this.jumpMarks = {}
    },
    mounted: function () {
      this.svg = SVG(this.$refs.simulator).panZoom({zoomMin: 0.1})
      this.svg.node.classList.add('simulation')
      this.simulation = this.svg.group()

      this.loading = true

      inkStitch.get('stitch_plan').then(response => {
        this.stitchPlan = response.data
        let [minx, miny, maxx, maxy] = this.stitchPlan.bounding_box
        let width = maxx - minx
        let height = maxy - miny
        this.svg.viewbox(0, 0, width, height);

        this.stitchPlan.color_blocks.forEach(color_block => {
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

        this.numStitches = this.stitches.length - 1
        this.generateMarks()
        this.generateColorSections()
        this.loading = false

        // v-on:keydown doesn't seem to work, maybe an Electron issue?
        Mousetrap.bind("up", this.animationSpeedUp)
        Mousetrap.bind("down", this.animationSlowDown)
        Mousetrap.bind("left", this.animationReverse)
        Mousetrap.bind("right", this.animationForward)
        Mousetrap.bind("space", this.toggleAnimation)
        Mousetrap.bind("+", this.animationForwardOneStitch)
        Mousetrap.bind("-", this.animationBackwardOneStitch)

        this.start()
        this.showColorChanges = true
      })
    }
  }
</script>

<style lang="css" scoped>
   @import '../assets/style/simulator.css'
</style>
