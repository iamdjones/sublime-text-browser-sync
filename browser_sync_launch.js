var argv = require('minimist')(process.argv.slice(2));
var bs = require('browser-sync').create('ST3');

setTimeout(startUp,0)

function startUp(){
	bs.init({
	server:argv.server,
	files:argv.files.split(','),
	index:argv.index,
	startPath:argv.startPath,
	logLevel:"silent",
	browser:"chrome"
	});
}

console.log('finished');
