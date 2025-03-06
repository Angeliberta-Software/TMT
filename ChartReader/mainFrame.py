import MetaTrader5 as mt5
import wx
import logging


logger = logging.getLogger(__name__)

class MainFrame(wx.Frame):
	def __init__(self):
		super().__init__(parent=None, title="TMT")
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.ctrlpanel = wx.Panel(self)
		ctrlpanel_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.initialize_btn = wx.Button(self.ctrlpanel, label="initialize MetaTrader")
		ctrlpanel_sizer.Add(self.initialize_btn, 0, wx.ALL | wx.CENTER, 5)
		self.initialize_btn.Bind(wx.EVT_BUTTON, self.on_press)
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
		self.Show()

	def on_press(self, event):
		if not mt5.initialize():
			wx.MessageBox('Failed to initialize mt5. Try again.', 'Error', wx.OK | wx.ICON_ERROR)
			logger.error('Failed to initialize MT5 connection.')
			mt5.shutdown()
		else:
			self.label1.Label = f'mt5 version: {mt5.version()}'
			self.label2.Label = str(mt5.terminal_info())
