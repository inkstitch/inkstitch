<template>
  <div class="simulator">
    <div class="simulation"></div>
    <div class="display">
      speed: {{speedDisplay}} stitches/sec   current stitch: {{currentStitchDisplay}}/{{numStitches}}  command: {{currentCommand}}
    </div>
    <div class="controls">
      <button v-on:click="animationSpeedUp">&gt;&gt;</button>
      <button v-on:click="animationSlowDown">&lt;&lt;</button>
    </div>
  </div>
</template>

<script>
  const inkStitch = require("../../lib/api")
  const Mousetrap = require("mousetrap")
  const SVG = require("svg.js")
  require("svg.panzoom.js")

  export default {
    name: 'simulator',
    data: function() {
      return {
        speed: 16,
        currentStitch: 1,
        direction: 1,
        numStitches: 0,
        animating: false
      }
    },
    computed: {
      currentStitchDisplay() {
        return this.currentStitch.toFixed()
      },
      speedDisplay() {
        return this.speed * this.direction
      },
      currentCommand() {
        let stitch = this.stitches[this.currentStitch.toFixed()]

        if (stitch === undefined) {
          return ""
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
      }
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
      toggleAnimation() {
        if (this.animating) {
          this.stop()
        } else {
          this.start()
        }
      },
      animationForwardOneFrame() {
        this.stop()
        this.currentStitch++
        this.clampCurrentStitch()
        this.renderFrame()
      },
      animationBackwardOneFrame() {
        this.stop()
        this.currentStitch--
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
      this.svg = SVG(this.$el.querySelector(".simulation")).size("90%", "85%").panZoom({zoomMin: 0.1})
      this.simulation = this.svg.group()

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

        // v-on:keydown doesn't seem to work, maybe an Electron issue?
        Mousetrap.bind("up", this.animationSpeedUp)
        Mousetrap.bind("down", this.animationSlowDown)
        Mousetrap.bind("left", this.animationReverse)
        Mousetrap.bind("right", this.animationForward)
        Mousetrap.bind("space", this.toggleAnimation)
        Mousetrap.bind("+", this.animationForwardOneFrame)
        Mousetrap.bind("-", this.animationBackwardOneFrame)

        this.start()
      })
  	}
  }
</script>

<style>
  /* CSS */
</style>