# NVDA Add-on: Talking Meta Trader 
# Copyright (C) 2026, Angeliberta Software
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import sys

PLUGIN_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(PLUGIN_DIR, "lib")
if LIB_DIR not in sys.path:
	sys.path.insert(0, LIB_DIR)

import MetaTrader5 as mt5
import appModuleHandler
import api
from scriptHandler import script
from logHandler import log
from ui import message
from controlTypes import role
import addonHandler
from datetime import datetime
from . import reader
from . import instruments


try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")


class AppModule(appModuleHandler.AppModule):

	GESTURE_CATEGORY_NAME = "TMT"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not mt5.initialize():
			log.error("Failed to connect to MT5")
			mt5.shutdown()
		else:
			log.info(f'MT5 connected. Version: {mt5.version()}')
		self.ruler = instruments.Ruler()
		self.announceCrossingLevels = False

	def getElements(self):
		return api.getForegroundObject().children

	def processTitle(self):
		titleElements = api.getForegroundObject().name.split("-")
		return titleElements[len(titleElements) - 1].strip()

	# Translators: Gesture description.
	@script(description=_("Announce current profile"), gesture="kb:control+p", category=GESTURE_CATEGORY_NAME)
	def script_announceCurrentProfile(self, gesture):
		message(self.getElements()[10].children[0].children[1].name)

	@script(gesture="kb:nvda+t")
	def script_fixWindowTitle(self, gesture):
		message(self.processTitle())

	# Translators: Gesture description.
	@script(description=_("Focus on toolbox window"), gesture="kb:control+1", category=GESTURE_CATEGORY_NAME)
	def script_focusOnToolboxWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Toolbox":
				obj.children[2].setFocus()
				break

	# Translators: Gesture description.
	@script(description=_("Focus on data window"), gesture="kb:control+2", category=GESTURE_CATEGORY_NAME)
	def script_focusOnDataWindow(self, gesture):
		self.getElements()[1].setFocus()

	# Translators: Gesture description.
	@script(description=_("Focus on navigator window"), gesture="kb:control+3", category=GESTURE_CATEGORY_NAME)
	def script_focusOnNavigatorWindow(self, gesture):
		self.getElements()[3].children[1].setFocus()

	# Translators: Gesture description.
	@script(description=_("Focus on market watch window"), gesture="kb:control+4", category=GESTURE_CATEGORY_NAME)
	def script_focusOnMarketWatchWindow(self, gesture):
		self.getElements()[4].children[0].setFocus()

	# Translators: Gesture description.
	@script(description=_("Focus on Workspace"), gesture="kb:control+5", category=GESTURE_CATEGORY_NAME)
	def script_focusOnWorkspace(self, gesture):
		for obj in self.getElements():
			if obj.name == "Workspace":
				obj.setFocus()
				break

	# Translators: Gesture description.
	@script(description=_("Announce terminal time"), gesture="kb:control+0", category=GESTURE_CATEGORY_NAME)
	def script_announceTerminalTime(self, gesture):
		data = self.getElements()[4].name.split(':')
		text = f"{data[1]}:{data[2]}:{data[3]}"
		message(text)

	# Translators: Gesture description.
	@script(description=_("Show toolbox tabs."), gesture="kb:control+shift+1", category=GESTURE_CATEGORY_NAME)
	def script_showToolboxTabs(self, gesture):
		for obj in self.getElements():
			if obj.name == "Toolbox":
				obj.children[0].setFocus()
				break

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == role.Role.PANE:
			data = self.processTitle()
			message(data)
			reader.recieve_data(data)
		nextHandler()

	# Translators: Gesture description.
	@script(description=_("Send symbol and timeframe info to chart reader app"), gesture="kb:control+shift+0", category=GESTURE_CATEGORY_NAME)
	def script_callChartReader(self, gesture):
		data = self.processTitle()
		reader.recieve_data(data)

	# Translators: Gesture description.
	@script(description=_("Speak current chart info"), gesture="kb:control+I", category=GESTURE_CATEGORY_NAME)
	def script_chartInfo(self, gesture):
		if not reader.symbol == "" or not reader.timeFrame== "":
			message(f"{reader.symbol} {reader.timeFrame}")
		else:
			message("Currently there is no any chart data loaded.")

	# Translators: Gesture description.
	@script(description=_("Go to first bar"), gesture="kb:control+shift+Q", category=GESTURE_CATEGORY_NAME)
	def script_goToFirstBar(self, gesture):
		reader.playFirstBar()

	# Translators: Gesture description.
	@script(description=_("Go to last bar"), gesture="kb:control+shift+E", category=GESTURE_CATEGORY_NAME)
	def script_goToLastBar(self, gesture):
		reader.playLastBar()

	# Translators: Gesture description.
	@script(description=_("Go 5 bars back"), gesture="kb:shift+Q", category=GESTURE_CATEGORY_NAME)
	def script_goTo5BarsBack(self, gesture):
		reader.goXBarsBack(5)

	# Translators: Gesture description.
	@script(description=_("Go 5 bars forward"), gesture="kb:shift+E", category=GESTURE_CATEGORY_NAME)
	def script_goTo5BarsForvard(self, gesture):
		reader.goXBarsForward(5)

	# Translators: Gesture description.
	@script(description=_("Go 12 bars back"), gesture="kb:control+Q", category=GESTURE_CATEGORY_NAME)
	def script_goTo12BarsBack(self, gesture):
		reader.goXBarsBack(12)

	# Translators: Gesture description.
	@script(description=_("Go 12 bars forward"), gesture="kb:control+E", category=GESTURE_CATEGORY_NAME)
	def script_goTo12BarsForward(self, gesture):
		reader.goXBarsForward(12)

	# Translators: Gesture description.
	@script(description=_("Previous bar"), gesture="kb:Q", category=GESTURE_CATEGORY_NAME)
	def script_previousBar(self, gesture):
		reader.playPreviousBar()
		crossingLevel = instruments.getCrossingLevel(reader.getCurrentBarInfo(reader.LOW_COLUMN), reader.getCurrentBarInfo(reader.HIGH_COLUMN))
		if not crossingLevel == 0 and self.announceCrossingLevels: message(f'Crossing level {crossingLevel}')

	# Translators: Gesture description.
	@script(description=_("Next bar"), gesture="kb:E", category=GESTURE_CATEGORY_NAME)
	def script_nextBar(self, gesture):
		reader.playNextBar()
		crossingLevel = instruments.getCrossingLevel(reader.getCurrentBarInfo(reader.LOW_COLUMN), reader.getCurrentBarInfo(reader.HIGH_COLUMN))
		if not crossingLevel == 0 and self.announceCrossingLevels: message(f'Crossing level {crossingLevel}')

	# Translators: Gesture description.
	@script(description=_("Use ruler by open price"), gesture="kb:control+A", category=GESTURE_CATEGORY_NAME)
	def script_useRulerByOpen(self, gesture):
		self.processRuler(reader.getCurrentBarInfo(reader.OPEN_COLUMN), reader.currentBar)

	# Translators: Gesture description.
	@script(description=_("Use ruler by close price"), gesture="kb:control+D", category=GESTURE_CATEGORY_NAME)
	def script_useRulerByClose(self, gesture):
		self.processRuler(reader.getCurrentBarInfo(reader.CLOSE_COLUMN), reader.currentBar)

	# Translators: Gesture description.
	@script(description=_("Use ruler by low price"), gesture="kb:control+S", category=GESTURE_CATEGORY_NAME)
	def script_useRulerByLow(self, gesture):
		self.processRuler(reader.getCurrentBarInfo(reader.LOW_COLUMN), reader.currentBar)

	# Translators: Gesture description.
	@script(description=_("Use ruler by high price"), gesture="kb:control+W", category=GESTURE_CATEGORY_NAME)
	def script_useRulerByHigh(self, gesture):
		self.processRuler(reader.getCurrentBarInfo(reader.HIGH_COLUMN), reader.currentBar)

	# Translators: Gesture description.
	@script(description=_("Add level by low price"), gesture="kb:shift+s", category=GESTURE_CATEGORY_NAME)
	def script_addLevelByLow(self, gesture):
		price = reader.getCurrentBarInfo(reader.LOW_COLUMN)
		instruments.addLevel(price)
		message(f'Added level: {price}')

	# Translators: Gesture description.
	@script(description=_("Add level by high price"), gesture="kb:shift+W", category=GESTURE_CATEGORY_NAME)
	def script_addLevelByHigh(self, gesture):
		price = reader.getCurrentBarInfo(reader.HIGH_COLUMN)
		instruments.addLevel(price)
		message(f'Added level: {price}')

	# Translators: Gesture description.
	@script(description=_("Add level by open price"), gesture="kb:shift+A", category=GESTURE_CATEGORY_NAME)
	def script_addLevelByOpen(self, gesture):
		price = reader.getCurrentBarInfo(reader.OPEN_COLUMN)
		instruments.addLevel(price)
		message(f'Added level: {price}')

	# Translators: Gesture description.
	@script(description=_("Add level by close price"), gesture="kb:shift+D", category=GESTURE_CATEGORY_NAME)
	def script_addLevelByClose(self, gesture):
		price = reader.getCurrentBarInfo(reader.CLOSE_COLUMN)
		instruments.addLevel(price)
		message(f'Added level: {price}')

	# Translators: Gesture description.
	@script(description=_("Delete level"), gesture="kb:shift+L", category=GESTURE_CATEGORY_NAME)
	def script_deleteLevel(self, gesture):
		if instruments.deleteLevel(): message('Level deleted.')
		else: message('No levels.')

	# Translators: Gesture description.
	@script(description=_("Next level"), gesture="kb:T", category=GESTURE_CATEGORY_NAME)
	def script_nextLevel(self, gesture):
		self.processLevels(1)

	# Translators: Gesture description.
	@script(description=_("Previous level"), gesture="kb:G", category=GESTURE_CATEGORY_NAME)
	def script_previousLevel(self, gesture):
		self.processLevels(-1)

	# Translators: Gesture description.
	@script(description=_("Closest level"), gesture="kb:L", category=GESTURE_CATEGORY_NAME)
	def script_closestLevel(self, gesture):
		closestLevel = instruments.getClosestLevel(reader.getCurrentPrice())
		if not closestLevel == 0: message(str(closestLevel))
		else: message('No levels')

	# Translators: Gesture description.
	@script(description=_("Say open price"), gesture="kb:A", category=GESTURE_CATEGORY_NAME)
	def script_sayOpenPrice(self, gesture):
		message(str(reader.getCurrentBarInfo(reader.OPEN_COLUMN)))

	# Translators: Gesture description.
	@script(description=_("Say close price"), gesture="kb:D", category=GESTURE_CATEGORY_NAME)
	def script_sayClosePrice(self, gesture):
		message(str(reader.getCurrentBarInfo(reader.CLOSE_COLUMN)))

	# Translators: Gesture description.
	@script(description=_("Say low"), gesture="kb:S", category=GESTURE_CATEGORY_NAME)
	def script_sayLow(self, gesture):
		message(str(reader.getCurrentBarInfo(reader.LOW_COLUMN)))

	# Translators: Gesture description.
	@script(description=_("Say high"), gesture="kb:W", category=GESTURE_CATEGORY_NAME)
	def script_sayHigh(self, gesture):
		message(str(reader.getCurrentBarInfo(reader.HIGH_COLUMN)))

	# Translators: Gesture description.
	@script(description=_("Say date"), gesture="kb:F", category=GESTURE_CATEGORY_NAME)
	def script_sayDate(self, gesture):
		message(str(datetime.utcfromtimestamp(reader.getCurrentBarInfo(reader.TIME_COLUMN))))

	# Translators: Gesture description.
	@script(description=_("Say volume"), gesture="kb:V", category=GESTURE_CATEGORY_NAME)
	def script_sayVolume(self, gesture):
		message(str(reader.getCurrentBarInfo(reader.TICK_VOLUME_COLUMN)))

	# Translators: Gesture description.
	@script(description=_("Say current price"), gesture="kb:C", category=GESTURE_CATEGORY_NAME)
	def script_sayCurrentPrice(self, gesture):
		message(str(reader.getCurrentPrice()))

	# Translators: Gesture description.
	@script(description=_("Play preview"), gesture="kb:P", category=GESTURE_CATEGORY_NAME)
	def script_playPreview(self, gesture):
		reader.playPreview()

	# Translators: Gesture description.
	@script(description=_("Delete a marker"), gesture="kb:shift+M", category=GESTURE_CATEGORY_NAME)
	def script_deleteMarker(self, gesture):
		result = instruments.deleteMarker(reader.getCurrentBarInfo(reader.TIME_COLUMN))
		if result: message('Marker deleted.')
		else: message('No marker selected.')

	# Translators: Gesture description.
	@script(description=_("Plase a marker"), gesture="kb:M", category=GESTURE_CATEGORY_NAME)
	def script_placeMarker(self, gesture):
		instruments.addMarker(reader.getCurrentBarInfo(reader.TIME_COLUMN))
		message('Marker set')

	# Translators: Gesture description.
	@script(description=_("Go to next marker"), gesture="kb:]", category=GESTURE_CATEGORY_NAME)
	def script_goToNextMarker(self, gesture):
		self.processMarkers(1)

	# Translators: Gesture description.
	@script(description=_("Go to previous marker"), gesture="kb:[", category=GESTURE_CATEGORY_NAME)
	def script_goToPreviousMarker(self, gesture):
		self.processMarkers(-1)

	# Translators: Gesture description.
	@script(description=_("Toggle announce crossing levels"), gesture="kb:control+L", category=GESTURE_CATEGORY_NAME)
	def script_toggleAnnounceCrossingLevels(self, gesture):
		if self.announceCrossingLevels:
			self.announceCrossingLevels = False
			message('Announce crossing levels off')
		else:
			self.announceCrossingLevels = True
			message('Announce crossing levels on')

	# Translators: Gesture description.
	@script(description=_("Toggle play high/low"), gesture="kb:control+C", category=GESTURE_CATEGORY_NAME)
	def script_togglePlayHighLow(self, gesture):
		if reader.play_high_low:
			reader.play_high_low = False
			message('Play high/low off')
		else:
			reader.play_high_low = True
			message('Play high/low on')

	def processMarkers(self, direction):
		date = 0
		if direction == 1: date = instruments.nextMarker()
		if direction == -1: date = instruments.previousMarker()
		if not date == 0:
			for i in range(0, len(reader.dataSet)):
				if reader.dataSet[i][reader.TIME_COLUMN] == date:
					reader.goToBarById(i)

	def processRuler(self, price, barIndex):
		if not self.ruler.activated:
			self.ruler.activate(price, barIndex)
			message('Ruler start marker set.')
		else:
			priceDifference, barDifference = self.ruler.calculate(price, barIndex)
			message(f'{str(priceDifference)}, {str(barDifference)}')

	def  processLevels(self, direction):
		price = 0
		if direction == 1: price = instruments.nextLevel()
		if direction == -1: price = instruments.previousLevel()
		if not price == 0: message(str(price))
		else: message('No levels.')
