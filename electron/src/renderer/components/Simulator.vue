<template>
  <div ref="simulator" class="simulator vld-parent">
    <fieldset>
      <div class="window-controls">
        <div ref="controlInfoButton" class="control-info-button" v-on:click="toggleInfo">
          <font-awesome-icon icon="info"/>
          <collapse-transition>
            <div class="control-info" v-show="infoExpanded" v-bind:style="{'max-height': infoMaxHeight + 'px'}">
              <h1>
                <font-awesome-icon icon="info" class="info-icon"/>
                <translate>Simulator Shortcut Keys</translate>
              </h1>
              <div>
                <div>
                  <p>
                    <translate>Button</translate>
                  </p>
                  <p>
                    <translate>Function</translate>
                  </p>
                  <p>
                    <translate>Shortcut Key</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="pause" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Pause</translate>
                  </p>
                  <p>
                    <translate>Space</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="play" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play</translate>
                  </p>
                  <p>P</p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="angle-double-left" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play backward</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for left arrow keyboard key">← Arrow left</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="angle-double-right" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play forward</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for right arrow keyboard key">→ Arrow right</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="shoe-prints" class="fa-button fa-flip-horizontal"/>
                  </p>
                  <p>
                    <translate translate-comment="description of keyboard shortcut that moves one stitch backward in simulator">
                      One step backward
                    </translate>
                  </p>
                  <p>-
                    <translate translate-comment="name for this keyboard key: -">Minus</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="shoe-prints" class="fa-button"/>
                  </p>
                  <p>
                    <translate translate-comment="description of keyboard shortcut that moves one stitch forward in simulator">
                      One step forward
                    </translate>
                  </p>
                  <p>
                    <translate translate-comment="name for this keyboard key: +">+ Plus</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="step-backward" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Jump to previous command</translate>
                  </p>
                  <p><translate translate-comment="name for page down keyboard key">Page down (PgDn)</translate></p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="step-forward" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Jump to next command</translate>
                  </p>
                  <p><translate translate-comment="name for page up keyboard key">Page up (PgUp)</translate></p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="hippo" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Slow down</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for down arrow keyboard key">↓ Arrow down</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="horse" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Speed up</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for up arrow keyboard key">↑ Arrow up</translate>
                  </p>
                </div>
              </div>
            </div>
          </collapse-transition>
        </div>
        <div class="toggle-controls" v-on:click="toggleControls">
          <font-awesome-icon v-if="controlsExpanded" icon="minus"/>
          <font-awesome-icon v-else icon="plus"/>
        </div>
      </div>
      <collapse-transition>
        <div class="panel" v-show="controlsExpanded">
          <fieldset class="controls">
            <legend>
              <translate>Controls</translate>
            </legend>
            <button v-on:click="stop" :class="{pressed: paused}" :title="$gettext('Pause (space)')">
              <font-awesome-icon icon="pause" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="start" :class="{pressed: animating}" :title="$gettext('Play (arrow left | arrow right)')">
              <font-awesome-icon icon="play" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationReverse" :class="{pressed: reverse}" :title="$gettext('Play backward (arrow left)')">
              <font-awesome-icon icon="angle-double-left" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
            </button>
            <button v-on:click="animationForward" :class="{pressed: forward}" :title="$gettext('Play forward (arrow right)')">
              <font-awesome-icon icon="angle-double-right" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
            </button>
            <button v-on:click="animationBackwardOneStitch" :title="$gettext('One step backward (-)')">
              <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button fa-flip-horizontal"/>
            </button>
            <button v-on:click="animationForwardOneStitch" :title="$gettext('One step forward (+)')">
              <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationPreviousCommand" :title="$gettext('Jump to previous command (Page down)')">
              <font-awesome-icon icon="step-backward" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationNextCommand" :title="$gettext('Jump to next command (Page up)')">
              <font-awesome-icon icon="step-forward" size="2x" class="fa-button"/>
            </button>
          </fieldset>
          <fieldset class="speed">
            <legend>
              <translate :translate-n="speed" translate-plural="Speed: %{speed} stitches/sec">Speed: %{speed} stitch/sec</translate>
            </legend>
            <button v-on:click="animationSlowDown" :title="$gettext('Slow down (arrow down)')">
              <font-awesome-icon icon="hippo" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationSpeedUp" :title="$gettext('Speed up (arrow up)')">
              <font-awesome-icon icon="align-right" class="fa-motion-lines"/>
              <font-awesome-icon icon="horse" size="2x" class="fa-button fa-fast"/>
            </button>
          </fieldset>
          <fieldset class="command">
            <legend>
              <translate>Command</translate>
            </legend>
            <span class="current-command">{{currentCommand}}</span>
          </fieldset>
          <fieldset class="show-commands">
            <legend>Show</legend>
            <span>
              <input id="trim-checkbox" type="checkbox" v-model="showTrims"/>
              <label for="trim-checkbox"><font-awesome-icon icon="cut"/> <translate>trims</translate></label>
              <br/>
              <input id="jump-checkbox" type="checkbox" v-model="showJumps"/>
              <label for="jump-checkbox"><font-awesome-icon icon="frog"/> <translate>jumps</translate></label>
            </span>
            <span>
              <input id="color-change-checkbox" type="checkbox" v-model="showColorChanges"/>
              <label for="color-change-checkbox"><font-awesome-icon icon="exchange-alt"/> <translate>color changes</translate></label>
              <br/>
              <input id="stop-checkbox" type="checkbox" v-model="showStops"/>
              <label for="stop-checkbox"><font-awesome-icon icon="pause"/> <translate>stops</translate></label>
            </span>
            <span class="npp">
            <input id="npp-checkbox" type="checkbox" v-model="showNeedlePenetrationPoints"/>
            <label for="npp-checkbox">
              <font-awesome-layers>
                <font-awesome-icon icon="circle" transform="shrink-9"/>
                <font-awesome-icon icon="minus" class="fa-thin-line"/>
              </font-awesome-layers>
              <span v-translate>needle<br/>points</span>
            </label>
          </span>
          </fieldset>
        </div>
      </collapse-transition>
      <div class="slider-container">
        <span>1</span>
        <span class="slider-box">
          <vue-slider
              :value="currentStitchDisplay"
              @change="setCurrentStitch"
              :min="0"
              :max="numStitches"
              :duration="0"
              :marks="sliderMarks"
              :process="sliderProcess">
            <template v-slot:label="mark">
              <div :class="['vue-slider-mark-label', `slider-label-${mark.command}`, { active: mark.active }]">
                <font-awesome-icon :icon="mark.icon"/>
              </div>
            </template>
          </vue-slider>
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
        <div class="loading-text">
          <translate>Rendering stitch-plan...</translate>
        </div>
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

  function SliderMark(command, icon) {
    this.label = ""
    this.command = command
    this.icon = icon
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
        controlsExpanded: true,
        infoExpanded: false,
        infoMaxHeight: 0,
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
        showStops: false,
        showNeedlePenetrationPoints: false
      }
    },
    watch: {
      currentStitch: throttle(function () {
        this.currentStitchDisplay = Math.floor(this.currentStitch)
      }, 100, {leading: true, trailing: true}),
      showNeedlePenetrationPoints: function () {
        if (this.needlePenetrationPoints === null) {
          return;
        }

        this.needlePenetrationPoints.forEach(npp => {
          if (this.showNeedlePenetrationPoints) {
            npp.show()
          } else {
            npp.hide()
          }
        })
      }
    },
    computed: {
      speedDisplay() {
        return this.speed * this.direction
      },
      currentCommand() {
        let stitch = this.stitches[Math.floor(this.currentStitch)]

        if (stitch === undefined || stitch === null) {
          return ""
        }

        let label = "STITCH"
        switch (true) {
          case stitch.jump:
            label = this.$gettext("JUMP")
            break
          case stitch.trim:
            label = this.$gettext("TRIM")
            break
          case stitch.stop:
            label = this.$gettext("STOP")
            break
          case stitch.color_change:
            label = this.$gettext("COLOR CHANGE")
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
      toggleInfo() {
        this.infoExpanded = !this.infoExpanded;
        this.infoMaxHeight = this.$refs.controlInfoButton.getBoundingClientRect().top;
      },
      toggleControls() {
        this.controlsExpanded = !this.controlsExpanded;
      },
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
          this.$refs.currentStitchInput.value = Math.floor(this.currentStitch)
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
        this.currentStitch = Math.max(Math.min(this.currentStitch, this.numStitches), 0)
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

        while (this.renderedStitch > this.currentStitch) {
          this.stitchPaths[this.renderedStitch].hide();
          this.renderedStitch -= 1
        }

        this.moveCursor()
      },
      shouldAnimate() {
        if (this.direction == 1 && this.currentStitch < this.numStitches) {
          return true;
        } else if (this.direction == -1 && this.currentStitch > 0) {
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
      resizeCursor() {
        // This makes the cursor stay the same size when zooming in or out.
        // I'm not exactly sure how it works, but it does.
        this.cursor.size(25 / this.svg.zoom())
        this.cursor.stroke({width: 2 / this.svg.zoom()})

        // SVG.js seems to move the cursor when we resize it, so we need to put
        // it back where it goes.
        this.moveCursor()

        this.adjustScale()
      },
      moveCursor() {
        let stitch = this.stitches[Math.floor(this.currentStitch)]
        if (stitch === null || stitch === undefined) {
          this.cursor.hide()
        } else {
          this.cursor.show()
          this.cursor.center(stitch.x, stitch.y)
        }
      },
      adjustScale: throttle(function () {
          let one_mm = 96 / 25.4 * this.svg.zoom();
          let scaleWidth = one_mm
          let simulatorWidth = this.$refs.simulator.getBoundingClientRect().width
          let maxWidth = Math.min(simulatorWidth / 2, 300)

          while (scaleWidth > maxWidth) {
            scaleWidth /= 2.0
          }

          while (scaleWidth < 100) {
            scaleWidth += one_mm
          }

          let scaleMM = scaleWidth / one_mm

          this.scale.plot(`M0,0 v10 h${scaleWidth / 2} v-5 v5 h${scaleWidth / 2} v-10`)

          // round and strip trailing zeros, source: https://stackoverflow.com/a/53397618
          let mm = scaleMM.toFixed(8).replace(/([0-9]+(\.[0-9]+[1-9])?)(\.?0+$)/, '$1')
          this.scaleLabel.text(`${mm} mm`)
        }, 100, {leading: true, trailing: true}
      ),
      generateMarks() {
        this.commandList = Array()
        for (let i = 1; i < this.stitches.length; i++) {
          if (this.stitches[i].trim) {
            this.trimMarks[i] = new SliderMark("trim", "cut")
            this.commandList.push(i)
          } else if (this.stitches[i].stop) {
            this.stopMarks[i] = new SliderMark("stop", "pause")
            this.commandList.push(i)
          } else if (this.stitches[i].jump) {
            this.jumpMarks[i] = new SliderMark("jump", "frog")
            this.commandList.push(i)
          } else if (this.stitches[i].color_change) {
            this.colorChangeMarks[i] = new SliderMark("color-change", "exchange-alt")
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
      },
      generateMarker(color) {
        return this.svg.marker(3, 3, add => {
          let needlePenetrationPoint = add.circle(3).fill(color).hide()
          this.needlePenetrationPoints.push(needlePenetrationPoint)
        })
      },
      generateScale() {
        let svg = SVG(this.$refs.simulator)
        svg.node.classList.add("simulation-scale")
        this.scale = svg.path("M0,0").stroke({color: "black", width: "1px"}).fill("none")
        this.scaleLabel = svg.text("0 mm").move(0, 12)
        this.scaleLabel.node.classList.add("simulation-scale-label")
      },
      generateCursor() {
        this.cursor =
          this.svg.path("M0,0 v2.8 h1.2 v-2.8 h2.8 v-1.2 h-2.8 v-2.8 h-1.2 v2.8 h-2.8 v1.2 h2.8")
          .stroke({
            width: 0.1,
            color: '#FFFFFF',
          })
          .fill('#000000')
        this.cursor.node.classList.add("cursor")
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
      this.needlePenetrationPoints = []
      this.cursor = null
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
          let color = `${color_block.color.visible_on_white.hex}`
          let path_attrs = {fill: "none", stroke: color, "stroke-width": 0.3}
          let marker = this.generateMarker(color)

          let stitching = false
          let prevStitch = null
          color_block.stitches.forEach(stitch => {
            stitch.x -= minx
            stitch.y -= miny

            let path = null
            if (stitching && prevStitch) {
              path = this.simulation.path(`M${prevStitch.x},${prevStitch.y} ${stitch.x},${stitch.y}`).attr(path_attrs).hide()
            } else {
              path = this.simulation.path(`M${stitch.x},${stitch.y} ${stitch.x},${stitch.y}`).attr(path_attrs).hide()
            }
            path.marker('end', marker)
            this.stitchPaths.push(path)
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
        this.generateScale()
        this.generateCursor()

        this.loading = false

        // v-on:keydown doesn't seem to work, maybe an Electron issue?
        Mousetrap.bind("up", this.animationSpeedUp)
        Mousetrap.bind("down", this.animationSlowDown)
        Mousetrap.bind("left", this.animationReverse)
        Mousetrap.bind("right", this.animationForward)
        Mousetrap.bind("pagedown", this.animationPreviousCommand)
        Mousetrap.bind("pageup", this.animationNextCommand)
        Mousetrap.bind("space", this.toggleAnimation)
        Mousetrap.bind("+", this.animationForwardOneStitch)
        Mousetrap.bind("-", this.animationBackwardOneStitch)

        this.svg.on('zoom', this.resizeCursor)
        this.resizeCursor()

        this.start()
      })
    }
  }
</script>

<style src="../assets/style/simulator.css" scoped></style>
