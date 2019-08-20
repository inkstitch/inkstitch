const inkStitch = require("./lib/api")
const SVG = require("svg.js")
//inkStitch.get('ping').then(response => { document.querySelector("#content").innerHTML = response.data })

var fps = document.getElementById("fps")
//var frame = 0

var container = document.getElementById("simulation")
var simulation = SVG("simulation").size(800, 800)
//const black_stroke = {fill: "none", stroke: "black"}
////var x = 0
////var y = 10
//
//var paths = Array()
//
//for (let y = 0; y < 800; y += 10) {
//	for (let x = 0; x < 800; x += 1) {
//		paths.push(simulation.path(`M${x},${y} ${x},${y + 10}`).attr(black_stroke).hide());
//	}
//}
//
//var i = 0;
//
//setInterval(function() {
//	let now = performance.now()
//	let frame_time = (now - last_tick) / 1000.0;
//	last_tick = now
//
//	let segments = 300 * frame_time;
//	
//	fps.innerHTML = `${segments} ${frame_time}`
//	
//	for (let j=0; j < segments; j++) {
//    	    paths[i].show();
//	    i++;
//	}
//}, 33);

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
	console.log(performance.now() - starts)

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


