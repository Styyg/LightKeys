const express = require('express')
const bodyParser = require("body-parser")
const fs = require('fs')
const app = express()
const port = 3000

app.use(express.static(__dirname + '/public'))
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.post('/send', (req, res) => {
	try {
		fs.writeFileSync(__dirname + '/public/settings.json', JSON.stringify(req.body))
		res.status(200).send()
	} catch (error) {
		res.status(400).send('Error while updating settings')

	}
})

app.listen(port, () => {
	console.log(`Example app listening at http://localhost:${port}`)
})