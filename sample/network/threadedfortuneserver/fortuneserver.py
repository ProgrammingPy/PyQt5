import sys
from PyQt5.QtCore import (QCoreApplication, QByteArray, QDataStream,
	qrand)
from PyQt5.QtNetwork import QTcpServer, QTcpSocket
from fortunethread import FortuneThread

class FortuneServer(QTcpServer):
	"""docstring for Server"""
	def __init__(self, parent=None):
		super(FortuneServer, self).__init__(parent)
		self.fortunes = ("You've been leading a dog's life. Stay off the furniture.",
					"You've got to think about tomorrow.",
					"You will be surprised by a loud noise.",
					"You will feel hungry again in another hour.",
					"You might have mail.",
					"You cannot kill time without injuring eternity.",
					"Computers are not intelligent. They only think they are.")
	
	def incomingConnection(self, sockDescriptor):
		fortune = self.fortunes[qrand() % len(self.fortunes)]
		thread = FortuneThread(sockDescriptor, fortune, self)
		#print('%s' %(fortune))
		thread.finished.connect(thread.deleteLater)
		thread.start() 


if __name__ == '__main__':
	app = QCoreApplication(sys.argv)
	server = FortuneServer()
	if not server.listen():
		print('listening error')
		app.exit()
	print('listening to port %d' %(server.serverPort()))
	app.exec_()