import logging
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import webbrowser


logger = logging.getLogger(__name__)

symbol = ""
timeFrame = ""
dataSet = []

# Settings
NUMBER_OF_BARS_TO_RECIEVE = 200

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

# Callback for server
def recieve_data(serverMessage):
	global symbol, timeFrame, dataSet
	symbol, timeFrame = serverMessage[1:-1].split(",")
	dataSet = mt5.copy_rates_from_pos(symbol, getMt5TimeFrame(timeFrame), 0, NUMBER_OF_BARS_TO_RECIEVE)
	print(dataSet)
