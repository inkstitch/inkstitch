const inkStitch = require("./lib/api")
const SVG = require("svg.js")

var fps = document.getElementById("fps")

let svg_width = window.innerWidth * 0.9
let svg_height = window.innerHeight * 0.85

var container = document.getElementById("simulation")
var svg = SVG("simulation").size(svg_width, svg_height)
var simulation = svg.group()

var stitches = Array()

inkStitch.get('stitch_plan').then(response => {
	container.style.display = "none"
	
	var stitch_plan = response.data
    let [minx, miny, maxx, maxy] = stitch_plan.bounding_box    
	
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

	let width = maxx - minx
    let height = maxy - miny
    let scale_x = svg_width / width
    let scale_y = svg_height / height
    let scale = Math.min(scale_x, scale_y)
    
    simulation.move((svg_width - scale * width) / 2.0, (svg_height - scale * height) / 2.0)
    simulation.scale(scale, scale)
    
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


