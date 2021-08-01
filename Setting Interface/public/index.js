const leds_settings = {
  color: "#FF0000",
  brightness: 100,
};

function changeColor(e) {
  leds_settings.color = e.target.value;
}

async function init() {
  const inputRGB = document.getElementById("colorRGB");
  const brightness = document.getElementById("brightness");
  inputRGB.addEventListener("change", changeColor);

  const response = await fetch("./leds_settings.json");
  const data = await response.json();
  inputRGB.value = data.colorRGB;
  brightness.value = data.brightness;
}

init();
