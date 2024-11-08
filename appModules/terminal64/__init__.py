import appModuleHandler
import api
from scriptHandler import script
from logHandler import log
from ui import message
from controlTypes import role


class AppModule(appModuleHandler.AppModule):

	GESTURE_CATEGORY_NAME = "TMT"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def getElements(self):
		return api.getForegroundObject().children

	def processTitle(self):
		titleElements = api.getForegroundObject().name.split("-")
		return titleElements[len(titleElements) - 1].strip()

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

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == role.Role.PANE:
			message(self.processTitle())
		nextHandler()
