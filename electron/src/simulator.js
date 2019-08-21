const inkStitch = require("./lib/api")
const SVG = require("svg.js")
require("svg.panzoom.js")

var fps = document.getElementById("fps")

var container = document.getElementById("simulation")
var svg = SVG("simulation").size("90%", "85%").panZoom({zoomMin: 0.1})
var simulation = svg.group()

var stitches = Array()

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
    
    var i = 0;
	var last_tick = performance.now()

	var interval = setInterval(function() {
		let now = performance.now()
		let frame_time = (now - last_tick) / 1000.0;
		last_tick = now

		let segments = 300 * frame_time;
		
		fps.innerHTML = `${segments} ${frame_time}`
		
		for (let j=0; j < segments && i < stitches.length; j++) {
	    	    stitches[i].show();
		    i++;
		}
		
		if (i >= stitches.length) {
		    clearInterval(interval);
		}
	}, 33);
	
})


