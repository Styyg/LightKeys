function init() {
	setEventsListeners()
	getSettings().then((settings) => {
		setSettings(settings)
	})
	getPresets().then((presets) => {
		showPresets(presets)
	})
}

async function getSettings() {
	const response = await fetch('./settings.json')
	const settings = await response.json()
	return settings
}

async function getPresets() {
	const response = await fetch('./presets.json')
	const presets = await response.json()
	return presets
}

function setEventsListeners() {
	const btnValidate = document.getElementById('btn-validate')
	const colorRGBRangeInput = document.getElementById('colorRGBRangeInput')
	const colorRGBTextInput = document.getElementById('colorRGBTextInput')
	const colorWRangeInput = document.getElementById('colorWRangeInput')
	const colorWTextInput = document.getElementById('colorWTextInput')
	const brightnessRangeInput = document.getElementById('brightnessRangeInput')
	const brightnessTextInput = document.getElementById('brightnessTextInput')

	btnValidate.addEventListener('click', (e) => {
		saveSettings()
	})

	colorRGBRangeInput.addEventListener('input', (e) => {
		colorRGBTextInput.value = e.target.value
	})
	colorRGBTextInput.addEventListener('input', (e) => {
		colorRGBRangeInput.value = e.target.value
	})

	colorWRangeInput.addEventListener('input', (e) => {
		colorWTextInput.value = e.target.value
	})
	colorWTextInput.addEventListener('input', (e) => {
		colorWRangeInput.value = e.target.value
	})

	brightnessRangeInput.addEventListener('input', (e) => {
		brightnessTextInput.value = e.target.value
	})
	brightnessTextInput.addEventListener('input', (e) => {
		brightnessRangeInput.value = e.target.value
	})
}

function showPresets(presets) {
	const presetsList = document.querySelector('.presetsList')

	for (const preset of presets) {
		const btn = document.createElement('button')
		btn.classList.add('btn', 'btn-outline-warning')
		btn.innerText = preset.name
		btn.addEventListener('click', (e) => {
			setSettings(preset.settings)
		})
		presetsList.append(btn)
	}
}

function setSettings(settings) {
	const colorRGBRangeInput = document.getElementById('colorRGBRangeInput')
	const colorRGBTextInput = document.getElementById('colorRGBTextInput')
	const colorWRangeInput = document.getElementById('colorWRangeInput')
	const colorWTextInput = document.getElementById('colorWTextInput')
	const brightnessRangeInput = document.getElementById('brightnessRangeInput')
	const brightnessTextInput = document.getElementById('brightnessTextInput')

	colorRGBRangeInput.value = colorRGBTextInput.value = settings.colorRGB
	colorWRangeInput.value = colorWTextInput.value = settings.colorW
	brightnessRangeInput.value = brightnessTextInput.value = settings.brightness
}

async function saveSettings() {
	const colorRGBRangeInput = document.getElementById('colorRGBRangeInput')
	const colorWRangeInput = document.getElementById('colorWRangeInput')
	const brightnessRangeInput = document.getElementById('brightnessRangeInput')
	const settings = {
		colorRGB: colorRGBRangeInput.value,
		colorW: colorWRangeInput.value,
		brightness: brightnessRangeInput.value,
	}

	const response = await fetch('/send', {
		method: 'POST',
		body: JSON.stringify(settings),
		headers: {
			'Content-Type': 'application/json',
		},
	})
}

init()
