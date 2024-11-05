import appModuleHandler
import tones

class AppModule(appModuleHandler.AppModule):

	def event_gainFocus(self, obj, nextHandler):
		tones.beep(256, 200)