const inkStitch = require("./lib/api")
const SVG = require("svg.js")
require("svg.panzoom.js")
const Mousetrap = require("mousetrap")

var fps = document.getElementById("fps")

var container = document.getElementById("simulation")
var svg = SVG("simulation").size("90%", "85%").panZoom({zoomMin: 0.1})
var simulation = svg.group()

var stitches = Array()

var speed = 16
const target_fps = 30
const target_frame_period = 1000.0 / target_fps

inkStitch.get('stitch_plan').then(response => {
	container.style.display = "none"
	
	var stitch_plan = response.data
    let [minx, miny, maxx, maxy] = stitch_plan.bounding_box    
    let width = maxx - minx
    let height = maxy - miny    
    svg.viewbox(0, 0, width, height);
	
	console.log(stitch_plan)
	stitch_plan.color_blocks.forEach(color_block => {
		let attrs = {fill: "none", stroke: `${color_block.color.visible_on_white.hex}`, "stroke-width": 0.3}
		let prevStitch = null
		color_block.stitches.forEach(stitch => {
		    stitch.x -= minx
		    stitch.y -= miny
		    if (stitch.trim) {
		        prevStitch = null
		    } else if (stitch.color_change) {
		        // ignore
		    } else {
        			if (prevStitch) {
        				stitches.push(simulation.path(`M${prevStitch.x},${prevStitch.y} ${stitch.x},${stitch.y}`).attr(attrs).hide())
        			}
        			prevStitch = stitch
		    }
		})
	})

	container.style.display = "";
    
	var last_frame_start = performance.now()
	var current_stitch = 1
	var rendered_stitch = 0
	var direction = 1

	var renderFrame = function() {
		let frame_start = performance.now();
		let frame_time = frame_start - last_frame_start
		last_frame_start = frame_start
		
		let num_stitches = speed * Math.max(frame_time, target_frame_period) / 1000.0;
		current_stitch = Math.max(Math.min(current_stitch + num_stitches * direction, stitches.length - 1), 0)
		
        //fps.innerHTML = `${num_stitches.toFixed(2)} ${last_frame_time.toFixed(2)}`
		
		while (rendered_stitch + 1 <= current_stitch) {
		    rendered_stitch += 1
		    stitches[rendered_stitch].show();
		}
		
		while (rendered_stitch - 1 >= current_stitch) {
		    stitches[rendered_stitch].hide();
		    rendered_stitch -= 1
		}
		
		fps.innerHTML = `${num_stitches.toFixed(2)} ${frame_time.toFixed(2)}`
		
		if (current_stitch < stitches.length - 1) {
		    setTimeout(renderFrame, Math.max(0, target_frame_period - frame_time))
		}
	}
	
	renderFrame()
	
	Mousetrap.bind("up", () => {
	    speed *= 2.0
        console.log(speed)
	})
	
	Mousetrap.bind("down", () => {
	    speed /= 2.0
	    speed = Math.max(speed, 1)
	    
	    console.log(speed)
	})
	
	Mousetrap.bind("right", () => {
	    direction = 1
	})

    Mousetrap.bind("left", () => {
        direction = -1
    })
})


