const inkStitch = require("./lib/api")
const SVG = require("svg.js")

var fps = document.getElementById("fps")

var container = document.getElementById("simulation")
var simulation = SVG("simulation").size("90%", "85%")

var stitches = Array()

inkStitch.get('simulator/get_stitch_plan').then(response => {
	var start = performance.now()
	container.style.display = "none"
	
	var stitch_plan = response.data
	console.log(stitch_plan)
	stitch_plan.stitch_blocks.forEach((stitch_block, i) => {
		let attrs = {fill: "none", stroke: `#${stitch_plan.colors[i]}`}
		let prevStitch = null
		stitch_block.forEach(stitch => {
			if (prevStitch) {
				stitches.push(simulation.path(`M${prevStitch.join(',')} ${stitch.join(',')}`).attr(attrs).hide())
			}
			prevStitch = stitch
		})
	})
	console.log(performance.now() - start)

	container.style.display = "";

	var i = 0;
	var last_tick = performance.now()

	setInterval(function() {
		let now = performance.now()
		let frame_time = (now - last_tick) / 1000.0;
		last_tick = now

		let segments = 300 * frame_time;
		
		fps.innerHTML = `${segments} ${frame_time}`
		
		for (let j=0; j < segments; j++) {
	    	    stitches[i].show();
		    i++;
		}
	}, 33);
	
})


