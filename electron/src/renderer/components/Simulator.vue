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
          :marks="sliderMarks"></vue-slider>
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

  // I should totally be able to set these on the prototype but then vue-slider
  // ignores them?!
  const markStyle = {
    display: "block",
    width: "4px",
    height: "20px",
    borderRadius: "4px",
    backgroundColor: "#808080",
    transform: "translate(0, -2px)"
  }
  const labelStyle = {
    "font-size": "2rem"
  }

  function SliderMark(label) {
    this.label = label
    this.style = markStyle
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
            this.trimMarks[i] = new SliderMark("✂")
            this.commandList.push(i)
          } else if (this.stitches[i].stop) {
            this.stopMarks[i] = new SliderMark("⏸")
            this.commandList.push(i)
          } else if (this.stitches[i].jump) {
            this.jumpMarks[i] = new SliderMark("↷")
            this.commandList.push(i)
          } else if (this.stitches[i].color_change) {
            this.colorChangeMarks[i] = new SliderMark("⇄")
            this.commandList.push(i)
          }
        }
      }
    },
    created: function () {
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

        this.numStitches = this.stitches.length - 1
        this.generateMarks()
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
    width: calc(100% - 12rem);
    margin-left: 10px;
    margin-right: 10px;
  }

  .current-stitch-input {
    width: 4rem;
    float: right;
    font-size: 1rem;
  }

  button {
    color: rgb(0, 51, 153)
  }

  .fa-spin-fast {
    animation: fa-spin 0.4s infinite linear;
  }

  .fa-button {
    margin: 3px;
  }

  .fa-fast {
    transform: skew(-15deg, -15deg) rotate(15deg) scale(1.25, 0.90);
  }

  .fa-motion-lines {
    transform: scale(1.0, 1.6) translate(0, -18%) skew(-15deg, -15deg) rotate(15deg);
  }

  .panel > * {
    display: inline-block;
    vertical-align: middle;
    text-align: center;
  }

  .panel fieldset {
    text-align: center;
    height: 50px;
  }

  fieldset {
    border-color: rgb(0, 51, 153);
  }

  fieldset button {
    display: inline-block;
  }

  fieldset.command span {
    font-family: sans-serif;
    font-size: 2rem;
    vertical-align: middle;
  }

  fieldset.command span.current-command {
    display: block;
    width: 18rem;
  }

  fieldset.show-commands {
    text-align: left;
  }

  fieldset.show-commands span {
    display: inline-block;
  }

  fieldset.show-commands span:first-of-type {
    padding-right: 12px;
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
    white-space: nowrap;
    text-align: center;
  }

  .slider-container {
    flex-grow: 0;
  }

  .simulator {
    display: flex;
    flex-direction: column;
    height: 95vh;
  }

  .current-command {
    color: rgb(0, 51, 153);
    font-weight: bold;
  }
</style>

<style>
  /* This is unscoped because the SVG tag isn't controlled by Vue and thus doesn't
     get the attribute used for scoping.  See:

     https://vue-loader.vuejs.org/guide/scoped-css.html
   */
  svg.simulation {
    flex-grow: 1;
    flex-shrink: 1;
    order: -1;
  }
</style>
