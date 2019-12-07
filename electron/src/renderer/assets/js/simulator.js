const inkStitch = require("../../../lib/api")
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
