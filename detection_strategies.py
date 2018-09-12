import numpy as np
from pyautogui import press, hotkey, click, scroll, typewrite, moveRel, moveTo, position
import pyautogui
pyautogui.FAILSAFE = False
import random
import operator
import audioop
import math
import time
import csv
import threading
centerXPos, centerYPos = position()

def loud_detection( data, label ):
	percent_met = data[-1][label]['percent'] >= 70
	
	if( percent_met ):
		return True
	else:
		return False

def medium_detection( data, label, required_percent, required_intensity ):
	last_is_not_label = data[-1][label]['percent'] < required_percent
	is_previous_label = data[-2][label]['percent'] >= required_percent and data[-2][label]['intensity'] >= required_intensity
	
	# Detect first signs of a medium length sound
	if( is_previous_label and last_is_not_label ):
		avg_percent = ( data[-2][label]['percent'] + data[-3][label]['percent'] + data[-4][label]['percent'] + data[-5][label]['percent'] + data[-6][label]['percent'] ) * 0.2
		avg_intensity = ( data[-2][label]['intensity'] + data[-3][label]['intensity'] + data[-4][label]['intensity'] + data[-5][label]['intensity'] + data[-6][label]['intensity'] ) * 0.2
		
		start_sound_not_label = data[-7][label]['percent'] < required_percent and data[-7][label]['intensity'] < required_intensity
		return avg_intensity >= required_intensity and avg_percent >= required_percent and start_sound_not_label
	return False		
		
def long_detection( data, label, required_percent, required_intensity ):
	last_is_not_label = data[-1][label]['percent'] < required_percent
	is_previous_label = data[-2][label]['percent'] >= required_percent and data[-2][label]['intensity'] >= required_intensity
	
	# Detect first signs of a long length sound
	if( is_previous_label and last_is_not_label ):
		avg_percent = ( data[-2][label]['percent'] + data[-3][label]['percent'] + data[-4][label]['percent'] + data[-5][label]['percent'] 
			+ data[-6][label]['percent'] + data[-7][label]['percent'] + data[-8][label]['percent'] + data[-9][label]['percent'] ) * 0.11
		avg_intensity = ( data[-2][label]['intensity'] + data[-3][label]['intensity'] + data[-4][label]['intensity'] + data[-5][label]['intensity'] 
			+ data[-6][label]['intensity'] + data[-7][label]['intensity'] + data[-8][label]['intensity'] + data[-9][label]['intensity'] ) * 0.11
				
		return avg_intensity >= required_intensity and avg_percent >= required_percent
	return False
		
def single_tap_detection( data, label, required_percent, required_intensity ):
	percent_met = data[-1][label]['percent'] >= required_percent
	rising_sound = data[-1][label]['intensity'] > data[-2][label]['intensity']
	first_sound = data[-2][label]['percent'] < required_percent
	previous_rising = data[-2][label]['percent'] >= required_percent and data[-2][label]['intensity'] < data[-3][label]['intensity']
	is_winner = data[-1][label]['winner']
	if( is_winner and percent_met and rising_sound and data[-1][label]['intensity'] >= required_intensity ):
		print( "Detecting single tap for " + label )
		return True
	else:
		return False

def no_detection( data, label ):
	peak_percent = np.max( [data[-1][label]['percent'], data[-2][label]['percent'], data[-3][label]['percent'], data[-4][label]['percent'], data[-5][label]['percent'], 
	data[-6][label]['percent'], data[-7][label]['percent'], data[-8][label]['percent'], data[-9][label]['percent']] )

	return peak_percent < 30
		
def quick_detection( currentDict, previousDict, label ):
	currentProbability = currentDict[ label ]
	if( currentProbability > 60 ):
		return True
	else:
		return False