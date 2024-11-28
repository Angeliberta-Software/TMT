import socket
from _thread import start_new_thread
from typing import Self
import appModuleHandler
import api
import contentRecog
import contentRecog.recogUi
import contentRecog.uwpOcr
from scriptHandler import script
from logHandler import log
from ui import message
from controlTypes import role


class AppModule(appModuleHandler.AppModule):

	GESTURE_CATEGORY_NAME = "TMT"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ocrRequested = False

	def getElements(self):
		return api.getForegroundObject().children

	def processTitle(self):
		titleElements = api.getForegroundObject().name.split("-")
		return titleElements[len(titleElements) - 1].strip()

	def callChartReader(self):
		client = socket.socket()
		hostName = socket.gethostname()
		port = 5678
		try:
			client.connect((hostName, port))
			data = self.processTitle().encode()
			client.send(data)
			response = client.recv(1024).decode()
			if not response == "ok":
				message("Failed to connect to chart reader")
				log.error("Failed to connect to chart reader")
			client.close()
		except Exception as e:
			message("Failed to connect to chart reader")
			log.error("Failed to connect to chart reader. " + str(e))

	@script(description="Announce current profile", gesture="kb:control+p", category=GESTURE_CATEGORY_NAME)
	def script_announceCurrentProfile(self, gesture):
		for o in self.getElements():
			if o.role == role.Role.STATUSBAR:
				message(o.children[1].name)
				break

	@script(gesture="kb:nvda+t")
	def script_fixWindowTitle(self, gesture):
		message(self.processTitle())

	@script(description="Focus on toolbox window", gesture="kb:control+1", category=GESTURE_CATEGORY_NAME)
	def script_focusOnToolboxWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Toolbox":
				obj.children[0].children[2].setFocus()
				break

	@script(description="Focus on data window", gesture="kb:control+2", category=GESTURE_CATEGORY_NAME)
	def script_focusOnDataWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[0].children[0].setFocus()
				break

	@script(description="Focus on navigator window", gesture="kb:control+3", category=GESTURE_CATEGORY_NAME)
	def script_focusOnNavigatorWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[1].children[1].setFocus()
				break

	@script(description="Focus on market watch window", gesture="kb:control+4", category=GESTURE_CATEGORY_NAME)
	def script_focusOnMarketWatchWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[2].children[0].setFocus()
				break

	@script(description="Focus on Workspace", gesture="kb:control+5", category=GESTURE_CATEGORY_NAME)
	def script_focusOnWorkspace(self, gesture):
		for obj in self.getElements():
			if obj.name == "Workspace":
				obj.setFocus()
				break

	@script(description="Announce terminal time", gesture="kb:control+0", category=GESTURE_CATEGORY_NAME)
	def script_announceTerminalTime(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				nameElements = obj.children[2].name.split(": ")
				message(nameElements[1])
				break

	@script(description="Show toolbox tabs.", gesture="kb:control+shift+1", category=GESTURE_CATEGORY_NAME)
	def script_showToolboxTabs(self, gesture):
		for obj in self.getElements():
			if obj.name == "Toolbox":
				self.ocrRequested = True
				obj.children[0].children[0].setFocus()
				break

	def event_gainFocus(self, obj, nextHandler):
		if self.ocrRequested:
			recognizor = contentRecog.uwpOcr.UwpOcr(None)
			contentRecog.recogUi.recognizeNavigatorObject(recognizor)
			self.ocrRequested = False
			return
		if obj.role == role.Role.PANE:
			message(self.processTitle())
		nextHandler()

	@script(description="Sends symbol and timeframe info to chart reader app", gesture="kb:control+shift+0", category=GESTURE_CATEGORY_NAME)
	def script_callChartReader(self, gesture):
		start_new_thread(AppModule.callChartReader, (self, ))
