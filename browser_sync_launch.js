var bs = require('browser-sync').create('ST3');

args = process.argv.slice(2);

bs.init({
	server:args[0],
	files:args[1].split(','),
	index:args[2],
	startPath:args[2],
	logLevel:"silent",
	browser:"chrome"
});