var http = require('http'),
    fs = require('fs');
var kuroshiro = require('kuroshiro');
var kuroshiro_analyzer_kuromoji=require("kuroshiro-analyzer-kuromoji");

fs.readFile('./card_create.html', function (err, html) {
    if (err) {
        throw err; 
    }       
    http.createServer(function(request, response) {  
        response.writeHeader(200, {"Content-Type": "text/html"});  
        response.write(html);  
        response.end();  
		console.log("RUNNING");
    }).listen(8000);
});