const leds_settings = {
    color: "#FF0000",
    brightness: 100
}

function changeColor(e) {
    leds_settings.color = e.target.value
    console.log(leds_settings)
    console.log(JSON.stringify(leds_settings))

// var data = new FormData();
// data.append("data" , "the_text_you_want_to_save");
// var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
// xhr.open( 'post', './save-settings.php', true );
// xhr.send(data);
}

function init() {
    const inputRGB = document.getElementById('colorRGB')
    inputRGB.addEventListener("change", changeColor)
}

init()