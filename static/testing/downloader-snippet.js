// Add a script html block and run the download.js file
// This is a snippet to be run in the chromium Sources/Snippets environment
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'static/testing/downloader.js';
document.head.appendChild(script);