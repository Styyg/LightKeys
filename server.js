var express = require('express')
var app = express()
var bodyParser = require('body-parser')
const fs = require('fs')

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static(__dirname + '/public'))

app.get('/', function (req, res) {
	res.sendFile(__dirname + '/index.html')
})

app.post('/process_post', urlencodedParser, function (req, res) {
	// Prepare output in JSON format
	output = {
		colorRGB: req.body.colorRGB,
		colorW: req.body.colorW,
		brightness: req.body.brightness,
	}
	fs.writeFileSync(__dirname + '/public/settings.json', JSON.stringify(output))
	res.status(200).send()
})

var server = app.listen(8081, function () {
	var port = server.address().port

	console.log('App listening at http://localhost:%s', port)
})
