import appModuleHandler
import api
from scriptHandler import script
from logHandler import log
from ui import message
from controlTypes import role

class AppModule(appModuleHandler.AppModule):

	#def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)

	def getElements(self):
		return api.getForegroundObject().children

	@script(description="Announce current profile", gesture="kb:control+p")
	def script_announceCurrentProfile(self, gesture):
		for o in self.getElements():
			if o.role == role.Role.STATUSBAR:
				message(o.children[1].name)
				break

	@script(gesture="kb:nvda+t")
	def script_fixWindowTitle(self, gesture):
		titleElements = api.getForegroundObject().name.split("-")
		msg = titleElements[len(titleElements) - 1].strip()
		message(msg)

	@script(description = "Focus on toolbox window", gesture="kb:control+1")
	def script_focusOnToolboxWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Toolbox":
				obj.children[0].children[2].setFocus()
				break

	@script(description="Focus on data window", gesture="kb:control+2")
	def script_focusOnDataWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[0].children[0].setFocus()
				break

	@script(description="Focus on navigator window", gesture="kb:control+3")
	def script_focusOnNavigatorWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[1].children[1].setFocus()
				break

	@script(description="Focus on market watch window", gesture="kb:control+4")
	def script_focusOnMarketWatchWindow(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				obj.children[2].children[0].setFocus()
				break

	@script(description="Focus on Workspace", gesture="kb:control+5")
	def script_focusOnWorkspace(self, gesture):
		for obj in self.getElements():
			if obj.name == "Workspace":
				obj.setFocus()
				break

	@script(description="Announce terminal time", gesture="kb:control+0")
	def script_announceTerminalTime(self, gesture):
		for obj in self.getElements():
			if obj.name == "Navigator":
				nameElements = obj.children[2].name.split(": ")
				message(nameElements[1])
				break