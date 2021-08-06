import time
import mido
import json
import os
import traceback
# from pathlib import Path
from os import stat
from rpi_ws281x import *
from enum import Enum

class Mode(Enum):
	PLAY = 0
	COLOR_RGB = 1
	COLOR_W = 2
	BRIGHTNESS = 3

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

	control = int(find_between(str(msg), "control=", " "))
	value = int(find_between(str(msg), "value=", " "))

	return note, vel, num_note, octave, led_offset, num_led, control, value

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

def read_settingsJSON(json_file_name):
	try:
		# Lecture du fichier settings.json
		with open(json_file_name, "r") as json_data:
			settings = json.load(json_data)
		return settings
	except Exception as e:
		print("read_settingsJSON :", e)
		return False

def get_settingsJSON(json_file_name):
	settings = read_settingsJSON(json_file_name)
	if(settings):
		try:
			rouge = int(settings["colorRGB"][1:3], 16)
			vert = int(settings["colorRGB"][3:5], 16)
			bleu = int(settings["colorRGB"][5:7], 16)
			blanc = int(settings["colorW"])
			brightness = int(settings["brightness"]) 
		except Exception as e:
			print("get_settingsJSON :", e)
			rouge = 255
			vert = 0
			bleu = 0
			blanc = 0
			brightness = 100

		return rouge, vert, bleu, blanc, brightness
	else:
		return 255, 0, 0, 0, 100

def write_settingsJSON(file_name, data):
	with open(file_name, "w") as json_file:
		json.dump(data, json_file)

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

def previewColorON(strip, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

def previewColorOFF(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, wheel(i))
	strip.show()

def selectionModeWhite(strip, color):
	bleu = color & 255
	rouge = (color >> 8) & 255
	vert = (color >> 16) & 255
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(vert, rouge, bleu, int(i * (255/strip.numPixels())) ))
		strip.show()


def previewColorW_ON(strip, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()
	
def previewColorW_OFF(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(vert, rouge, bleu, int(i * (255/strip.numPixels()))))
	strip.show()

def getDefaultSettingFileData():
	data = {
		"colorRGB": "#FF0000",
		"colorW": "0",
		"brightness": "100"
	}
	return data

def changeMode(mode):
	if(mode == Mode.PLAY.value):
		colorWipeFromCenter(strip, colorOFF)
	elif(mode == Mode.COLOR_RGB.value):
		rainbowFromCenter(strip)
	elif(mode == Mode.COLOR_W.value):
		selectionModeWhite(strip, colorON)
	elif(mode == Mode.BRIGHTNESS.value):
		colorWipeFromCenter(strip, colorON)
	# print("mode :", Mode(mode).name)
	return mode

#Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
#position des notes noires (en partant du la)
noire = {1, 4, 6, 9, 11}

dir_path = os.path.dirname(os.path.realpath(__file__))
json_file_name = dir_path + "/public/settings.json"
date_modif = stat(json_file_name)[8]


# LED strip configuration:
LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812_STRIP_RGBW


rouge, vert, bleu, blanc, LED_BRIGHTNESS = get_settingsJSON(json_file_name)
settings = read_settingsJSON(json_file_name)
if not(settings):
	settings = getDefaultSettingFileData()

# Color(G,R,B)   aucune idée de pourquoi c'est GRB au lieu de RGB, peut-être parce que les leds sont SK6812 au lieu de WS2812
colorON = Color(vert, rouge, bleu, blanc)
colorOFF = Color(0, 0, 0, 0)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

# Ouverture du port MIDI par l'interface USB
try:
	inport = mido.open_input('USB MIDI Interface:USB MIDI Interface MIDI 1 20:0')
except Exception as e:
	print(traceback.format_exc())

colorWipeFromCenter(strip, colorON) 
colorWipeFromSides(strip, Color(0,0,0,0)) 

mode = Mode.PLAY.value
# print("En attente d'entrée MIDI :")
try:
	while True:
		# Détecte les changements du fichier settings.json
		if(date_modif != stat(json_file_name)[8]):
			date_modif = stat(json_file_name)[8]
			# print("date_modif :", date_modif)
			time.sleep(0.05)
			# rouge, vert, bleu, blanc, LED_BRIGHTNESS = read_settingsJSON(json_file_name)
			rouge, vert, bleu, blanc, LED_BRIGHTNESS = get_settingsJSON(json_file_name)
			colorON = Color(vert, rouge, bleu, blanc)
			strip.setBrightness(LED_BRIGHTNESS)
			
			colorWipeFromCenter(strip, colorON) 
			colorWipeFromSides(strip, colorOFF) 

		for msg in inport.iter_pending():
			# print(msg)
			note, velocity, num_note, octave, led_offset, num_led, control, value = get_MIDI()

			# Mode PLAY : Jouer au piano et les leds s'allument
			if(mode == Mode.PLAY.value):
				#print("note", note, "num_note", num_note, "octave", octave, "num leds", num_led)
				if("note" in str(msg)):
					if(num_note in noire):
						bBlanche = False
					else:
						bBlanche = True

					# Allume ou éteint les leds
					if(int(velocity) > 0 and int(note) > 0):
						note_on(num_led, bBlanche)
					elif(int(velocity) == 0 and int(note) > 0):
						note_off(num_led, bBlanche)
				
				elif(control == 67 and value == 127):
					mode = changeMode(Mode.COLOR_RGB.value)

				elif(control == 66 and value == 127):
					mode = changeMode(Mode.BRIGHTNESS.value)

			# Mode COLOR_RGB : Les leds s'allument en arc en ciel, on peut choisir la couleur en appuyant sur une note
			elif(mode == Mode.COLOR_RGB.value):

				# NOTES DU PIANO : Choix des paramètres
				if "note_on" in str(msg):
					colorON_temp = wheel(num_led)
					previewColorON(strip, colorON_temp)
				elif "note_off" in str(msg):
					previewColorOFF(strip)

				# PEDALE DE GAUCHE : Changement de mode vers COLOR_W sans changer les paramètres
				elif(control == 67 and value == 127):
					mode = changeMode(Mode.COLOR_W.value)
					
				# PEDALE DU MILIEU : Changement de mode vers BRIGHTNESS sans changer les paramètres
				elif(control == 66 and value == 127):
					mode = changeMode(Mode.BRIGHTNESS.value)

				# PEDALE DE DROITE : Validation des paramètres
				elif(control == 64 and value == 127):
					colorON = colorON_temp
					bleu = colorON & 255
					rouge = (colorON >> 8) & 255
					vert = (colorON >> 16) & 255
					settings["colorRGB"] = "#" + '{:02x}'.format(rouge, 'x') + '{:02x}'.format(vert, 'x') + '{:02x}'.format(bleu, 'x')
					write_settingsJSON(json_file_name, settings)
					date_modif = stat(json_file_name)[8]
					mode = changeMode(Mode.PLAY.value)

			# Mode COLOR_W : Les leds s'allument avec la couleur choisie et différents degrés de blanc, on peut choisir la couleur en appuyant sur les notes
			elif(mode == Mode.COLOR_W.value):

				# NOTES DU PIANO : Choix des paramètres
				if "note_on" in str(msg):
					blanc_temp = int((note-21) * (255/87))
					previewColorW_ON(strip, Color(vert, rouge, bleu, blanc_temp))
				elif "note_off" in str(msg):
					previewColorW_OFF(strip)

				# PEDALE DE GAUCHE : Changement de mode vers PLAY sans changer les paramètres
				elif(control == 67 and value == 127):
					mode = changeMode(Mode.PLAY.value)
					
				# PEDALE DU MILIEU : Changement de mode vers BRIGHTNESS sans changer les paramètres
				elif(control == 66 and value == 127):
					mode = changeMode(Mode.BRIGHTNESS.value)

				# PEDALE DE DROITE : Validation des paramètres
				elif(control == 64 and value == 127):
					blanc = blanc_temp
					colorON = Color(vert, rouge, bleu, blanc)
					settings["colorW"] = blanc
					write_settingsJSON(json_file_name, settings)
					date_modif = stat(json_file_name)[8]
					mode = changeMode(Mode.PLAY.value)

			# Mode BRIGHTNESS : Les leds s'allument avec la couleur choisie, on peut choisir la luminosité en appuyant sur les notes
			elif(mode == Mode.BRIGHTNESS.value):

				# NOTES DU PIANO : Choix des paramètres
				if "note_on" in str(msg):
					brightness_temp = int((note-21) * (255/87))
					strip.setBrightness(brightness_temp)

				# PEDALE DE GAUCHE : Changement de mode vers COLOR_RGB sans changer les paramètres
				elif(control == 67 and value == 127):
					mode = changeMode(Mode.COLOR_RGB.value)
					
				# PEDALE DU MILIEU : Changement de mode vers PLAY sans changer les paramètres
				elif(control == 66 and value == 127):
					mode = changeMode(Mode.PLAY.value)

				# PEDALE DE DROITE : Validation des paramètres
				elif(control == 64 and value == 127):
					LED_BRIGHTNESS = brightness_temp
					strip.setBrightness(LED_BRIGHTNESS)
					settings["brightness"] = LED_BRIGHTNESS
					write_settingsJSON(json_file_name, settings)
					date_modif = stat(json_file_name)[8]
					mode = changeMode(Mode.PLAY.value)

		strip.show()

except: 
	# En cas d'erreur, le bandeau entier s'affiche en rouge
	print(traceback.format_exc())
	strip.setBrightness(50)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,255,0,0))
	strip.show()
	time.sleep(2)
	colorWipeFromCenter(strip, Color(0,0,0,0))

