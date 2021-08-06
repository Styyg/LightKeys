import time
import mido
import json
import os
from os import stat
from rpi_ws281x import *
from enum import Enum

class Mode(Enum):
	PLAY = 0
	COLOR = 1
	BRIGHTNESS = 2

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return False

def get_MIDI():
	#récupération de la valeur de la note (commence à 21 pour le LA tout à gauche d'un clavier 88 touches)
	note = int(find_between(str(msg), "note=", " "))
	
	#Récupération de la vélocité
	if "note_off" in str(msg):
		vel = 0
	else:
		vel = int(find_between(str(msg), "velocity=", " "))

	#numéro de la note au sein d'une octave (la: 0 laB: 11)
	num_note = (note-21)%12

	#numéro de l'octave, pour décaler l'affichage des leds
	octave = int((note-21) /12)

	#ajout d'un offset pour ajuster l'allumage des leds par rapport aux notes
	if(note > 93 or note == 84):
		led_offset = -2
	elif(note > 57):
		led_offset = -1
	else:
		led_offset = 0

	#numéro de la led à allumer, liée à la note jouée (commence à 0)
	num_led = tab_leds[num_note] + octave*24 + led_offset

	return note, vel, num_note, octave, led_offset, num_led

def note_on(led, blanche):
	strip.setPixelColor(led, colorON)
	strip.setPixelColor(led+1, colorON)
	if(blanche):
		strip.setPixelColor(led+2, colorON)

def note_off(led, blanche):
    strip.setPixelColor(led, colorOFF)
    strip.setPixelColor(led+1, colorOFF)
    if(blanche):
	    strip.setPixelColor(led+2, colorOFF)

def get_settingsJSON():
	try:
		# Lecture du fichier settings.json
		with open(dir_path + '/public/settings.json') as json_data:
			settings = json.load(json_data)
		rouge = int(settings["colorRGB"][1:3], 16)
		vert = int(settings["colorRGB"][3:5], 16)
		bleu = int(settings["colorRGB"][5:7], 16)
		blanc = int(settings["colorW"])
		brightness = int(settings["brightness"]) # Set to 0 for darkest and 255 for brightest
	except Exception as e:
		print("Erreur sur le fichier settings :", e)
		rouge = 255
		vert = 0
		bleu = 0
		blanc = 0
		brightness = 100 # Set to 0 for darkest and 255 for brightest
	
	return rouge, vert, bleu, blanc, brightness

def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def colorWipeFromCenter(strip, color):
	for i in range(int(strip.numPixels()/2) +1):
		strip.setPixelColor(int(strip.numPixels()/2) + i, color)
		strip.setPixelColor(int(strip.numPixels()/2) - i, color)
		strip.show()

def colorWipeFromSides(strip, color):
	for i in range(int(strip.numPixels()/2) +1):
		strip.setPixelColor(i, color)
		strip.setPixelColor(strip.numPixels() - i, color)
		strip.show()

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	fact = 255 / 59
	if pos < 59:
		return Color(int(pos * fact), int(255 - pos * fact), 0)
	elif pos < 118:
		pos -= 59
		return Color(int(255 - pos * fact), 0, int(pos * fact))
	else:
		pos -= 118
		return Color(0, int(pos * fact), int(255 - pos * fact))

def rainbow(strip):
	"""Draw rainbow that fades across all pixels at once."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, wheel(i))
	strip.show()
	
def rainbowFromCenter(strip):
	for i in range(int(strip.numPixels()/2) +1):
		strip.setPixelColor(int(strip.numPixels()/2) + i, wheel(int(strip.numPixels()/2) + i))
		strip.setPixelColor(int(strip.numPixels()/2) - i, wheel(int(strip.numPixels()/2) - i))
		strip.show()

def previewColor(strip, num_led, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

def previewColorOFF(strip, num_led):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, wheel(i))
	strip.show()


#Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
#position des notes noires (en partant du la)
noire = {1, 4, 6, 9, 11}

dir_path = os.path.dirname(os.path.realpath(__file__))
date_modif = stat(dir_path + "/public/settings.json")[8]


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

# Ouverture du port MIDI par l'interface USB
try:
	inport = mido.open_input('USB MIDI Interface:USB MIDI Interface MIDI 1 20:0')
except Exception as e:
	print("Erreur port MIDI :", e)

# Color(G,R,B)   aucune idée de pourquoi c'est GRB au lieu de RGB, peut-être parce que les leds sont SK6812 au lieu de WS2812
colorON = Color(vert, rouge, bleu, blanc)
colorOFF = Color(0, 0, 0, 0)

colorWipeFromCenter(strip, colorON) 
colorWipeFromSides(strip, Color(0,0,0,0)) 


mode = Mode.PLAY.value
print("En attente d'entrée MIDI :")
try:
	while True:
		# Détecte les changements du fichier settings.json
		if(date_modif != stat(dir_path + "/public/settings.json")[8]):
			date_modif = stat(dir_path + "/public/settings.json")[8]
			# print(date_modif)
			time.sleep(0.05)
			rouge, vert, bleu, blanc, LED_BRIGHTNESS = get_settingsJSON()
			colorON = Color(vert, rouge, bleu, blanc)
			strip.setBrightness(LED_BRIGHTNESS)
			
			colorWipeFromCenter(strip, colorON) 
			colorWipeFromSides(strip, colorOFF) 

		for msg in inport.iter_pending():
			# print(msg)
			note, velocity, num_note, octave, led_offset, num_led = get_MIDI()

			# Mode PLAY
			if("note" in str(msg) and mode == Mode.PLAY.value):
				#print("note", note, "num_note", num_note, "octave", octave, "num leds", num_led)
				if(num_note in noire):
					bBlanche = False
				else:
					bBlanche = True

				# Allume ou éteint les leds
				if(int(velocity) > 0 and int(note) > 0):
					note_on(num_led, bBlanche)
				elif(int(velocity) == 0 and int(note) > 0):
					note_off(num_led, bBlanche)

			# Mode SETTING
			else:
				control = int(find_between(str(msg), "control=", " "))
				value = int(find_between(str(msg), "value=", " "))

				# PEDALE DE GAUCHE : Changement de mode (COLOR ou BRIGHTNESS)
				if(control == 67 and value == 127):
					mode = (mode +1) %3

					if(mode == Mode.PLAY.value):
						colorWipeFromCenter(strip, colorOFF)
					elif(mode == Mode.COLOR.value): 
						rainbowFromCenter(strip)
						colorON_temp = colorON
					elif(mode == Mode.BRIGHTNESS.value):
						colorWipeFromCenter(strip, colorON)
						brightness_temp = strip.getBrightness()

					# print("mode :", Mode(mode).name)

				# PEDALE DU MILIEU : Validation du mode
				elif(control == 66 and value == 127 and mode != Mode.PLAY.value):
					if(mode == Mode.COLOR.value): 
						colorON = colorON_temp

					elif(mode == Mode.BRIGHTNESS.value):
						LED_BRIGHTNESS = brightness_temp
						strip.setBrightness(LED_BRIGHTNESS)

					colorWipeFromCenter(strip, colorOFF)
					mode = Mode.PLAY.value

				# NOTES DU PIANO : Choix des paramètres
				if "note_on" in str(msg):
					if(mode == Mode.COLOR.value):
						colorON_temp = wheel(num_led)
						previewColor(strip, num_led, colorON_temp)

					elif(mode == Mode.BRIGHTNESS.value):
						brightness_temp = int((note-21) * (255/87))
						strip.setBrightness(brightness_temp)

				elif "note_off" in str(msg):
					if(mode == Mode.COLOR.value):
						previewColorOFF(strip, num_led)

		strip.show()

except Exception as e: 
	# En cas d'erreur, le bandeau entier s'affiche en rouge
	print("Erreur lecture MIDI :", e)
	strip.setBrightness(50)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,255,0,0))
	strip.show()
	time.sleep(2)
	colorWipeFromCenter(strip, Color(0,0,0,0))

