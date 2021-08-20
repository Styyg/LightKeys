function init() {
	const btnValidate = document.querySelector('#btn-validate')
	const inputRGB = document.getElementById('colorRGB')
	const inputW = document.getElementById('colorW')
	const inputBrightness = document.getElementById('brightness')

	btnValidate.addEventListener('click', (e) => {
		saveDataInFile()
	})
	inputRGB.addEventListener('input', (e) => {
		showValueChange('colorRGB', 'span_RGB')
	})
	inputW.addEventListener('input', (e) => {
		showValueChange('colorW', 'span_W')
	})
	inputBrightness.addEventListener('input', (e) => {
		showValueChange('brightness', 'span_brightness')
	})

	readDataFromFile()

}

async function readDataFromFile() {
	const inputRGB = document.getElementById('colorRGB')
	const inputW = document.getElementById('colorW')
	const inputBrightness = document.getElementById('brightness')

	const response = await fetch('./settings.json')
	const data = await response.json()

	inputRGB.value = data.colorRGB
	inputW.value = data.colorW
	inputBrightness.value = data.brightness

	showValueChange('colorRGB', 'span_RGB')
	showValueChange('colorW', 'span_W')
	showValueChange('brightness', 'span_brightness')
}

async function saveDataInFile() {
	const inputRGB = document.getElementById('colorRGB')
	const inputW = document.getElementById('colorW')
	const inputBrightness = document.getElementById('brightness')
	const settings = {
		colorRGB: '#FF0000',
		colorW: 0,
		brightness: 100,
	}

	settings.colorRGB = inputRGB.value
	settings.colorW = inputW.value
	settings.brightness = inputBrightness.value

	const response = await fetch('/send',
		{
			method: 'POST', body: JSON.stringify(settings), headers: {
				"Content-Type": "application/json"
			}
		})
}

function showValueChange(elementValue, elementToShowValue) {
	document.getElementById(elementToShowValue).innerHTML =
		document.getElementById(elementValue).value
}

init()