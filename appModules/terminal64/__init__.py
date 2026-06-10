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
from . import reader


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
			message(self.processTitle())
		nextHandler()

	# Translators: Gesture description.
	@script(description=_("Send symbol and timeframe info to chart reader app"), gesture="kb:control+shift+0", category=GESTURE_CATEGORY_NAME)
	def script_callChartReader(self, gesture):
		data = self.processTitle()
		reader.recieve_data(data)
