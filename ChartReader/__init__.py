import MetaTrader5 as mt5
import wx
from mainFrame import MainFrame
import logging
from log_config import setup_logging
from server import Server


def serverCallBack(data):
	print(f'Data recieved: {data}')


if __name__ == '__main__':
	setup_logging()
	logger = logging.getLogger(__name__)

	logger.info('Starting server...')
	try:
		server = Server()
		server.callback = serverCallBack
		server.start()
	except Exception as e:
		logger.error('Failed to start server.', exc_info=True)
		wx.MessageBox('Failed to start server. Aborting...', 'Error', wx.OK | wx.ICON_ERROR)
		exit()

	logger.info('Initializing application GUI...')
	try:
		app = wx.App()
		frame = MainFrame()
		app.MainLoop()
	except Exception as e:
		logger.error('Failed to start GUI.', exc_info=True)
		wx.MessageBox('Failed to initialize GUI. Aborting...', 'Error', wx.OK | wx.ICON_ERROR)
		exit()

	logger.info('Disconnect from MT5')
	try:
		mt5.shutdown()
	except Exception as e:
		logger.error('Failed to disconnect from MT5', exc_info=True)

	try:
		logger.info('Stopping server...')
		server.stop()
	except Exception as e:
		logger.error('Failed to stop server.', exc_info=True)
