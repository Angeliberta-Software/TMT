import logging
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import webbrowser
import math
import winsound
import time
import threading
import wx
import instruments


logger = logging.getLogger(__name__)

# Globals
symbol = ""
timeFrame = ""
dataSet = []
currentBar = 0
lastBar = 0
maxPrice = 0
minPrice = 0

sound_isPlaying = False
soundThread = None

# Settings
number_of_bars_to_recieve = 100
play_high_low = False

# Constants
SOUND_MIN_FREQ = 120
SOUND_MAX_FREQ = 5000
SOUND_LENGTH = 150

# Table colums names
TIME_COLUMN = 'time'
OPEN_COLUMN = 'open'
HIGH_COLUMN = 'high'
LOW_COLUMN = 'low'
CLOSE_COLUMN = 'close'
TICK_VOLUME_COLUMN = 'tick_volume'
SPREAD_COLUMN = 'spread'
REAL_VOLUME_COLUMN = 'real_volume'

def getMt5TimeFrame(timeFrame):
	if timeFrame == "M1": return mt5.TIMEFRAME_M1
	if timeFrame == "M2": return mt5.TIMEFRAME_M2
	if timeFrame == "M3": return mt5.TIMEFRAME_M3
	if timeFrame == "M4": return mt5.TIMEFRAME_M4
	if timeFrame == "M5": return mt5.TIMEFRAME_M5
	if timeFrame == "M6": return mt5.TIMEFRAME_M6
	if timeFrame == "M10": return mt5.TIMEFRAME_M10
	if timeFrame == "M12": return mt5.TIMEFRAME_M12
	if timeFrame == "M15": return mt5.TIMEFRAME_M15
	if timeFrame == "M20": return mt5.TIMEFRAME_M20
	if timeFrame == "M30": return mt5.TIMEFRAME_M30
	if timeFrame == "H1": return mt5.TIMEFRAME_H1
	if timeFrame == "H2": return mt5.TIMEFRAME_H2
	if timeFrame == "H3": return mt5.TIMEFRAME_H3
	if timeFrame == "H4": return mt5.TIMEFRAME_H4
	if timeFrame == "H6": return mt5.TIMEFRAME_H6
	if timeFrame == "H8": return mt5.TIMEFRAME_H8
	if timeFrame == "H12": return mt5.TIMEFRAME_H12
	if timeFrame == "Daily": return mt5.TIMEFRAME_D1
	if timeFrame == "Weekly": return mt5.TIMEFRAME_W1
	if timeFrame == "Monthly": return mt5.TIMEFRAME_MN1
	return None

def priceToHerz(price):
	global maxPrice, minPrice
	freq = SOUND_MIN_FREQ + (price - minPrice) * (SOUND_MAX_FREQ - SOUND_MIN_FREQ) / (maxPrice - minPrice)
	return int(freq)

def createHTMLTable():
	dataFrame = pd.DataFrame(dataSet)
	dataFrame[TIME_COLUMN] = pd.to_datetime(dataFrame[TIME_COLUMN], unit='s')

	html = f'<html><head></head><body><h1>{symbol} {timeFrame}</h1>'
	html +=  dataFrame.to_html(index=False)
	html += '</body></html>'
	file_path = "chart.html"
	with open(file_path, "w", encoding="utf-8") as f:
		f.write(html)
		webbrowser.open(file_path)

def playSoundSequence():
	global sound_isPlaying
	if not sound_isPlaying: return
	winsound.Beep(priceToHerz(getCurrentBarInfo(OPEN_COLUMN)), SOUND_LENGTH)
	if not sound_isPlaying: return
	winsound.Beep(priceToHerz(getCurrentBarInfo(CLOSE_COLUMN)), SOUND_LENGTH)
	if not sound_isPlaying: return
	time.sleep(0.24)
	if play_high_low:
		if getCurrentBarInfo(OPEN_COLUMN) <= getCurrentBarInfo(CLOSE_COLUMN):
			if not sound_isPlaying: return
			winsound.Beep(priceToHerz(getCurrentBarInfo(LOW_COLUMN)), SOUND_LENGTH)
			if not sound_isPlaying: return
			winsound.Beep(priceToHerz(getCurrentBarInfo(HIGH_COLUMN)), SOUND_LENGTH)
		else:
			if not sound_isPlaying: return
			winsound.Beep(priceToHerz(getCurrentBarInfo(HIGH_COLUMN)), SOUND_LENGTH)
			if not sound_isPlaying: return
			winsound.Beep(priceToHerz(getCurrentBarInfo(LOW_COLUMN)), SOUND_LENGTH)
	sound_isPlaying = False

def playPreviewSequence():
	global sound_isPlaying, lastBar, dataSet
	i = 0
	while sound_isPlaying and i <= lastBar:
		winsound.Beep(priceToHerz(dataSet[i][CLOSE_COLUMN]), 100)
		i += 1
	sound_isPlaying = False

def playPreview():
	global sound_isPlaying, soundThread
	if sound_isPlaying:
		sound_isPlaying = False
		soundThread.join()
	soundThread = threading.Thread(target=playPreviewSequence)
	sound_isPlaying = True
	soundThread.start()

def playBar():
	global sound_isPlaying, soundThread
	if sound_isPlaying:
		sound_isPlaying = False
		soundThread.join()
	sound_isPlaying = True
	soundThread = threading.Thread(target=playSoundSequence)
	soundThread.start()

def playPreviousBar():
	global currentBar
	if currentBar == 0: return
	currentBar -= 1
	playBar()

def playNextBar():
	global currentBar
	if currentBar == lastBar: return
	currentBar += 1
	playBar()

def playFirstBar():
	global currentBar
	currentBar = 0
	playBar()

def playLastBar():
	global currentBar, lastBar
	currentBar = lastBar
	playBar()

def goXBarsBack(x):
	global currentBar
	if x >= currentBar: currentBar = 0
	else: currentBar -= x
	playBar()

def goXBarsForward(x):
	global currentBar, lastBar
	if currentBar + x >= lastBar: currentBar = lastBar
	else: currentBar += x
	playBar()

def goToBarById(id):
	global currentBar, lastBar
	if id >= 0 and id <= lastBar:
		currentBar = id
		playBar()

def getCurrentBarInfo(infoType):
	return dataSet[currentBar][infoType]

def getCurrentPrice():
	return mt5.copy_rates_from_pos(symbol, getMt5TimeFrame(timeFrame), 0, 1)[0][CLOSE_COLUMN]

# Callback for server
def recieve_data(serverMessage):
	global symbol, timeFrame, dataSet, currentBar, lastBar, maxPrice, minPrice
	try:
		logger.info(f'Parsing server message {serverMessage}')
		symbol, timeFrame = serverMessage[1:-1].split(",")
		logger.info(f'Parse result. Symbol: {symbol}. Timeframe: {timeFrame}')
		logger.info('Getting data from MT5...')
		dataSet = mt5.copy_rates_from_pos(symbol, getMt5TimeFrame(timeFrame), 0, number_of_bars_to_recieve)
		lastBar = len(dataSet) - 1
		currentBar = lastBar
		maxPrice = 0
		minPrice = math.inf
		for data in dataSet:
			if data[HIGH_COLUMN] > maxPrice: maxPrice = data[HIGH_COLUMN]
			if data[LOW_COLUMN] < minPrice: minPrice = data[LOW_COLUMN]
		logger.info(f'Last bar index: {lastBar}. Min price: {minPrice}. Max price: {maxPrice}')
		instruments.initialize(symbol, timeFrame )
		playBar()
	except Exception as e:
		logger.error('Unexpected error. ', exc_info=True)
		wx.MessageBox('Unexpected error. Please refer to logs.', 'Error', wx.OK | wx.ICON_ERROR)
