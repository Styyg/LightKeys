import time
import mido
import json
from os import stat

from rpi_ws281x import *

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return False

def note_on(led, blanche, vel):
    strip.setPixelColor(led, couleur)
    strip.setPixelColor(led+1, couleur)

    if(blanche):
	    strip.setPixelColor(led+2, couleur)

def note_off(led, blanche):
    strip.setPixelColor(led, couleur_fond)
    strip.setPixelColor(led+1, couleur_fond)

    if(blanche):
	    strip.setPixelColor(led+2, couleur_fond)

def get_settingsJSON():
	try:
		# Lecture du fichier settings.json
		with open('./public/settings.json') as json_data:
			settings = json.load(json_data)
		rouge = int(settings["colorRGB"][1:3], 16)
		vert = int(settings["colorRGB"][3:5], 16)
		bleu = int(settings["colorRGB"][5:7], 16)
		blanc = 0
		brightness = int(settings["brightness"]) # Set to 0 for darkest and 255 for brightest
	except:
		print("Erreur sur le fichier settings : application des valeurs color et brightness par défaut")
		rouge = 255
		vert = 136
		bleu = 0
		blanc = 0
		brightness = 100 # Set to 0 for darkest and 255 for brightest
	
	return rouge, vert, bleu, blanc, brightness

def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()


#Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
#position des notes noires (en partant du la)
noire = {1, 4, 6, 9, 11}

date_modif = stat("./public/settings.json")[8]


# LED strip configuration:
LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812_STRIP_RGBW

rouge, vert, bleu, blanc, LED_BRIGHTNESS = get_settingsJSON()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

# Ouverture du port MIDI 
ports = mido.get_input_names()
for port in ports:
	if "Through" not in port and "RPi" not in port and "RtMidOut" not in port:
		try:
			inport =  mido.open_input(port)
			# print("Inport set to "+port)
		except:
			print ("Failed to set "+port+" as inport")


# Color(G,R,B)   aucune idée de pourquoi c'est GRB au lieu de RGB, peut-être parce que les leds sont SK6812 au lieu de WS2812
couleur = Color(vert, rouge, bleu, blanc)
couleur_fond = Color(0, 0, 0, 0)

strip.setBrightness(100)
colorWipe(strip, Color(255,0,0,0)) 
colorWipe(strip, Color(0,0,0,0)) 

print("En attente d'entrée Midi")
try:
	while True:
		if(date_modif != stat("./public/settings.json")[8]):
			date_modif = stat("./public/settings.json")[8]
			# print(date_modif)
			# time.sleep(0.05)
			rouge, vert, bleu, blanc, LED_BRIGHTNESS = get_settingsJSON()
			couleur = Color(vert, rouge, bleu, blanc)
			strip.setBrightness(LED_BRIGHTNESS)
			
			colorWipe(strip, couleur)
			colorWipe(strip, couleur_fond)

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

			#ajout d'un offset pour ajuster l'allumage des leds par rapport aux notes
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
except: 
	strip.setBrightness(100)
	colorWipe(strip, Color(0,255,0,0)) 
	colorWipe(strip, Color(0,0,0,0))

