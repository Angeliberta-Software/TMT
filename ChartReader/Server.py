import socket
from _thread import start_new_thread
import logging


logger = logging.getLogger(__name__)

class Server:

	def __init__(self):
		self.server_socket = socket.socket()
		self.hostName = socket.gethostname()
		self.port = 5678
		self.server_socket.bind((self.hostName, self.port))
		self.callback = None
		self.isRunning = False

	def __processConnection(self):
		while True:
			if not self.isRunning:
				if isinstance(self.server_socket, socket.socket):
					self.server_socket.close()
				break

			try:
				connection, _ = self.server_socket.accept()
				data = connection.recv(1024)
				message = data.decode()
				logger.info("Received message: " + message)
				if not self.callback == None:
					self.callback(message)
				connection.send("ok".encode())
				connection.close()
			except Exception as e:
				logger.error("Failed to serve a connection.", exc_info=True)

	def start(self):
		self.isRunning = True
		self.server_socket.listen(1)
		start_new_thread(Server.__processConnection, (self, ))
		logger.info(f"Server started. Now listening on {self.hostName}:{self.port}")

	def stop(self):
		self.isRunning = False
		logger.info('Server stopped.')

# Example of use
"""
def callback(message):
	print("Callback is working. " + message)

s = Server()
s.callback = callback
s.start()
input("Any key to stop")
s.stop()
"""
