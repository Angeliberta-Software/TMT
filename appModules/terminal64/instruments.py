import logging
from pydantic import BaseModel
from typing import List
import json
import os
import math


class Ruler:
	def __init__(self):
		self.activated = False
		self.startPrice = 0
		self.endPrice = 0
		self.startBarIndex = 0
		self.endBarIndex = 0

	def activate(self, price, barIndex):
		self.startPrice = price
		self.startBarIndex = barIndex
		self.activated = True

	def calculate(self, price, barIndex):
		def decimal_places(x):
			s = str(x)
			if '.' in s:
				return len(s.split('.')[-1])
			else:
				return 0

		precision = max(decimal_places(self.startPrice), decimal_places(price))

		priceDifference = round(abs(self.startPrice - price), precision)
		barDifference = abs(self.startBarIndex - barIndex)
		self.activated = False
		return (priceDifference, barDifference)


class Storage(BaseModel):
	markers: List[int]
	levels : List[float]


logger = logging.getLogger(__name__)

storage = None
fileName = ''
currentMarker = 0
currentLevel = 0

def initialize(symbol, timeframe):
	global fileName, storage, currentMarker, currentLevel
	logger.info('Initializing instruments...')
	fileName = f'{symbol}_{timeframe}.json'
	logger.info(f'File to use: {fileName}')
	if os.path.isfile(fileName):
		logger.info('File exists, openning...')
		with open(fileName, 'r', encoding='utf-8') as f:
			jsonData = f.read()
			storage = Storage.model_validate_json(jsonData)
	else:
		logger.info('File does not exists, creating new object...')
		storage = Storage(markers=[], levels=[])
	currentMarker = 0
	currentLevel = 0

def updateFile():
	global storage, fileName
	try:
		with open(fileName, 'w', encoding='utf-8') as f:
			f.write(storage.model_dump_json(indent=4))
	except Exception as e:
		logger.error(f'Failed to write to file {fileName}.', exc_info=True)

def addMarker(date):
	global storage
	storage.markers.append(date)
	storage.markers.sort()
	updateFile()

def deleteMarker(date):
	global storage, currentMarker
	if date in storage.markers:
		storage.markers.remove(date)
		currentMarker = 0
		updateFile()
		return True
	else:
		return False

def nextMarker():
	global currentMarker, storage
	if not len(storage.markers) < 1:
		if not currentMarker >= len(storage.markers) - 1: currentMarker += 1
		return storage.markers[currentMarker]
	return 0

def previousMarker():
	global currentMarker, storage
	if not len(storage.markers) < 1:
		if not currentMarker <= 0: currentMarker -= 1
		return storage.markers[currentMarker]
	return 0

def addLevel(price):
	global storage
	storage.levels.append(price)
	storage.levels.sort()
	updateFile()

def deleteLevel():
	global storage, currentLevel
	if len(storage.levels) < 1: return False
	if currentLevel >= 0 and currentLevel < len(storage.levels):
		storage.levels.pop(currentLevel)
		currentLevel = 0
		updateFile()
		return True
	else:
		return False

def nextLevel():
	global currentLevel, storage
	if not len(storage.levels) < 1:
		if not currentLevel>= len(storage.levels) - 1:currentLevel+= 1
		return storage.levels[currentLevel]
	return 0

def previousLevel():
	global currentLevel, storage
	if not len(storage.levels) < 1:
		if not currentLevel<= 0: currentLevel-= 1
		return storage.levels[currentLevel]
	return 0

def getClosestLevel(currentPrice):
	global storage
	if len(storage.levels) < 1: return 0
	closestPrice = 0
	minDistance = math.inf
	for price in storage.levels:
		distance = abs(currentPrice - price)
		if distance < minDistance:
			minDistance = distance
			closestPrice = price
	return closestPrice

def getCrossingLevel(low, high):
	global storage
	if len(storage.levels) < 1: return 0
	for level in storage.levels:
		if level >= low and level <= high:
			return level
	return 0