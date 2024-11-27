import MetaTrader5 as mt5


if not mt5.initialize():
	print('Failed to initialize mt5')
	mt5.shutdown()
	quit()

print(mt5.terminal_info())
print(mt5.version())

mt5.shutdown()