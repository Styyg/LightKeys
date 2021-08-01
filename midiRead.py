#import time
import mido

from rpi_ws281x import *

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return False

def note_on(led, blanche, vel):
   # strip.setPixelColor(led, Color(int(vert * (vel/127)), int(rouge * (vel/127)), int(bleu * (vel/127)), int(blanc * (vel/127))))
   # strip.setPixelColor(led+1, Color(int(vert * (vel/127)), int(rouge * (vel/127)), int(bleu * (vel/127)), int(blanc * (vel/127))))
    strip.setPixelColor(led, couleur)
    strip.setPixelColor(led+1, couleur)

    if(blanche):
	    #strip.setPixelColor(led+2, Color(int(vert * (vel/127)), int(rouge * (vel/127)), int(bleu * (vel/127)), int(blanc * (vel/127))))
	    strip.setPixelColor(led+2, couleur)

def note_off(led, blanche):
    strip.setPixelColor(led, couleur_fond)
    strip.setPixelColor(led+1, couleur_fond)

    if(blanche):
	    strip.setPixelColor(led+2, couleur_fond)

#Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
	    #24, 27, 28, 31, 33, 34, 37, 38, 41, 43, 44, 47)

#position des notes noires (en partant du la)
noire = {1, 4, 6, 9, 11}

# LED strip configuration:
LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812_STRIP_RGBW


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()


ports = mido.get_input_names()

for port in ports:
	if "Through" not in port and "RPi" not in port and "RtMidOut" not in port:
		try:
			inport =  mido.open_input(port)
			print("Inport set to "+port)
		except:
			print ("Failed to set "+port+" as inport")

rouge = 255
vert = 80
bleu = 0
blanc = 0

# Color(G,R,B)
couleur = Color(vert, rouge, bleu, blanc)
#couleur_attenuee =  Color(int(vert/10), int(rouge/10), int(bleu/10), int(blanc/10))
couleur_fond = Color(3, 3, 3, 3)
#couleur_fond = Color(0, 0, 0, 0)

for i in range(0, LED_COUNT):
	strip.setPixelColor(i, couleur_fond)
	strip.show()

while True:
	for msg in inport.iter_pending():
		#récupération de la valeur de la note (commence à 21)
		note = int(find_between(str(msg), "note=", " "))
		#print(msg)
		#print(note)

		#numéro de la note au sein d'une octave (la: 0 laB: 11)
		num_note = (note-21)%12

		#numéro de l'octave, pour décaler l'affichage des leds
		octave = int((note-21) /12)

		#Récupération de la vélocité
		if "note_off" in str(msg):
			velocity = 0
		else:
			velocity = int(find_between(str(msg), "velocity=", " "))

		#ajout d'un offset pour ajuster l'alluamge des leds par rapport aux notes
		if(note > 93):
			led_offset = -2
		elif(note > 57):
			led_offset = -1
		else:
			led_offset = 0

		#exception sur certaines notes
		if(note == 84):
			led_offset -= 1

		#numéro de la led liée à la note (commence à 0)
		num_led = tab_leds[num_note] + octave*24 + led_offset

		if(num_note in noire):
			bBlanche = False
		else:
			bBlanche = True

		#print("note", note, "num_note", num_note, "octave", octave, "num leds", num_led)

		if(int(velocity) > 0 and int(note) > 0):
			note_on(tab_leds[num_note] + octave*24 + led_offset, bBlanche, velocity)
		elif(int(velocity) == 0 and int(note) > 0):
			note_off(tab_leds[num_note] + octave*24 + led_offset, bBlanche)
	strip.show()

