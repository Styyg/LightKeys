async function init() {
  const leds_settings = {
    color: "#FF0000",
    brightness: 100,
  };

  const inputRGB = document.getElementById("colorRGB");
  const brightness = document.getElementById("brightness");
  const form_settings = document.getElementById("form-settings");

  inputRGB.addEventListener("change", function (e) {
    leds_settings.color = e.target.value;
  });

  // form_settings.style.display = "none";
  const response = await fetch("./settings.json");
  const data = await response.json();
  console.log(data);
  inputRGB.value = data.colorRGB;
  brightness.value = data.brightness;
  // form_settings.style.display = "";
}

init();
