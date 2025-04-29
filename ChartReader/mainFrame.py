import MetaTrader5 as mt5
import wx
import logging
import reader
import accessible_output2.outputs
from datetime import datetime
import instruments


logger = logging.getLogger(__name__)

class MainFrame(wx.Frame):
	def __init__(self):
		super().__init__(parent=None, title="TMT")
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.ctrlpanel = wx.Panel(self)
		ctrlpanel_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.initialize_btn = wx.Button(self.ctrlpanel, label="initialize MetaTrader")
		ctrlpanel_sizer.Add(self.initialize_btn, 0, wx.ALL | wx.CENTER, 5)
		self.initialize_btn.Bind(wx.EVT_BUTTON, self.on_initialize_btn_press)
		self.initialize_btn.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

		self.showInTable_btn = wx.Button(self.ctrlpanel, label="Show in table...")
		ctrlpanel_sizer.Add(self.showInTable_btn, 0, wx.ALL | wx.CENTER, 5)
		self.showInTable_btn.Bind(wx.EVT_BUTTON, self.on_shoInTable_btn_press)
		self.showInTable_btn.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

		self.play_highlow_checkbox = wx.CheckBox(self.ctrlpanel, label='Play high-low')
		self.play_highlow_checkbox.SetValue(False)
		self.play_highlow_checkbox.Bind(wx.EVT_CHECKBOX, self.on_playHighLowCheckbox_press)
		self.play_highlow_checkbox.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
		ctrlpanel_sizer.Add(self.play_highlow_checkbox, 0, wx.ALL | wx.CENTER, 5)

		barsCountLabel = wx.StaticText(self.ctrlpanel, label='Bars count: ')
		self.barsCount_textCtrl = wx.TextCtrl(self.ctrlpanel, size=(200, -1))
		self.barsCount_textCtrl.Value = str(reader.number_of_bars_to_recieve)
		self.barsCount_textCtrl.Bind(wx.EVT_TEXT, self.on_barCountTextCtrl_change)
		ctrlpanel_sizer.Add(self.barsCount_textCtrl, 0, wx.ALL | wx.CENTER, 5)
		ctrlpanel_sizer.Add(barsCountLabel, 0, wx.ALL | wx.CENTER, 5)

		self.ctrlpanel.SetSizer(ctrlpanel_sizer)
		main_sizer.Add(self.ctrlpanel, 0, wx.ALL, 5)

		self.infopanel = wx.Panel(self)
		infopanel_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.label1 = wx.StaticText(self.infopanel, label=f'mt5 version: {mt5.version()}')
		self.label2 = wx.StaticText(self.infopanel, label='Terminal off')
		infopanel_sizer.Add(self.label1, 0, wx.ALL, 5)
		infopanel_sizer.Add(self.label2, 0, wx.ALL, 5)
		self.infopanel.SetSizer(infopanel_sizer)
		main_sizer.Add(self.infopanel, 0, wx.ALL, 5)

		self.SetSizer(main_sizer)

		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

		self.tts = accessible_output2.outputs.auto.Auto()
		self.ruler = instruments.Ruler()
		self.lastOutput = ''

		self.Show()

	def on_initialize_btn_press(self, event):
		logger.info('Initializing MT5 connection...')
		if not mt5.initialize():
			wx.MessageBox('Failed to initialize mt5. Try again.', 'Error', wx.OK | wx.ICON_ERROR)
			logger.error('Failed to initialize MT5 connection.')
			mt5.shutdown()
		else:
			self.label1.Label = f'mt5 version: {mt5.version()}'
			self.label2.Label = str(mt5.terminal_info())
			logger.info(f'MT5 version: {mt5.version()}. Terminal info: {mt5.terminal_info()}')

	def on_shoInTable_btn_press(self, event):
		reader.createHTMLTable()

	def on_key_down(self, event):
		keyCode = event.GetKeyCode()

		# Chart info
		if keyCode == ord('I') and event.ControlDown():
			if not reader.char == "" or not reader.timeFrame == "":
				self.tts.speak(f"{reader.char} {reader.timeFrame}")
			else:
				self.tts.speak("Currently there is no any chart data loaded.")
		# Go to first bar
		elif keyCode == ord('Q') and event.ControlDown() and event.ShiftDown(): reader.playFirstBar()
		# Go to last bar
		elif keyCode == ord('E') and event.ControlDown() and event.ShiftDown(): reader.playLastBar()
		# Go 5 bars back
		elif keyCode == ord('Q') and event.ShiftDown(): reader.goXBarsBack(5)()
		# Go 5 bars forward
		elif keyCode == ord('E') and event.ShiftDown(): reader.goXBarsForward(5)
		# Go 12 bars back
		elif keyCode == ord('Q') and event.ControlDown(): reader.goXBarsBack(12)
		# Go 12 bars forward
		elif keyCode == ord('E') and event.ControlDown(): reader.goXBarsForward(12)
		# Previous bar
		elif keyCode == ord('Q'): reader.playPreviousBar()
		# Next bar
		elif keyCode == ord('E'): reader.playNextBar()
		# Use ruler
		elif keyCode == ord('A') and event.ControlDown(): self.processRuler(reader.getCurrentBarInfo(reader.OPEN_COLUMN), reader.currentBar)
		# Use ruler
		elif keyCode == ord('D') and event.ControlDown(): self.processRuler(reader.getCurrentBarInfo(reader.CLOSE_COLUMN), reader.currentBar)
		# Use ruler
		elif keyCode == ord('S') and event.ControlDown(): self.processRuler(reader.getCurrentBarInfo(reader.LOW_COLUMN), reader.currentBar)
		# Use ruler
		elif keyCode == ord('W') and event.ControlDown(): self.processRuler(reader.getCurrentBarInfo(reader.HIGH_COLUMN), reader.currentBar)
		# Say open price
		elif keyCode == ord('A'): self.speak(str(reader.getCurrentBarInfo(reader.OPEN_COLUMN)))
		# Say close price
		elif keyCode == ord('D'): self.speak(str(reader.getCurrentBarInfo(reader.CLOSE_COLUMN)))
		# Say low
		elif keyCode == ord('S'): self.speak(str(reader.getCurrentBarInfo(reader.LOW_COLUMN)))
		# Say high
		elif keyCode == ord('W'): self.speak(str(reader.getCurrentBarInfo(reader.HIGH_COLUMN)))
		# Say date
		elif keyCode == ord('F'): self.speak(str(datetime.utcfromtimestamp(reader.getCurrentBarInfo(reader.TIME_COLUMN))))
		# Say volume
		elif keyCode == ord('V'): self.speak(str(reader.getCurrentBarInfo(reader.TICK_VOLUME_COLUMN)))
		# Say current price
		elif keyCode == ord('C'): self.speak(str(reader.getCurrentPrice()))
		# Say last output
		elif keyCode == ord('R'): self.tts.speak(self.lastOutput)
		# Play preview
		elif keyCode == ord('P'): reader.playPreview()
		# Delete a marker
		elif keyCode == ord('M') and event.ShiftDown():
			result = instruments.deleteMarker(reader.getCurrentBarInfo(reader.TIME_COLUMN))
			if result: self.speak('Marker deleted.')
			else: self.speak('No marker selected.')
		# Plase a marker
		elif keyCode == ord('M'):
			instruments.addMarker(reader.getCurrentBarInfo(reader.TIME_COLUMN))
			self.speak('Marker set')
		# Go to next marker
		elif keyCode == ord(']'): self.processMarkers(1)
		# Go to previous marker
		elif keyCode == ord('['): self.processMarkers(-1)
		# Let event go...
		else:
			event.Skip()

	def on_playHighLowCheckbox_press(self, event):
		if self.play_highlow_checkbox.GetValue():
			reader.play_high_low = True
		else:
			reader.play_high_low = False

	def on_barCountTextCtrl_change(self, event):
		try:
			reader.number_of_bars_to_recieve = int(self.barsCount_textCtrl.GetValue())
		except:
			logger.warn('Invalid user entry in bars count text control.')

	def processRuler(self, price, barIndex):
		if not self.ruler.activated:
			self.ruler.activate(price, barIndex)
			self.speak('Ruler start marker set.')
		else:
			priceDifference, barDifference = self.ruler.calculate(price, barIndex)
			self.speak(f'{str(priceDifference)}, {str(barDifference)}')

	def speak(self, string):
		self.tts.speak(string)
		self.lastOutput = string

	def processMarkers(self, direction):
		date = 0
		if direction == 1: date = instruments.nextMarker()
		if direction == -1: date = instruments.previousMarker()
		if not date == 0:
			for i in range(0, len(reader.dataSet)):
				if reader.dataSet[i][reader.TIME_COLUMN] == date:
					reader.goToBarById(i)
