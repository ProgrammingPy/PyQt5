import sys
from PyQt5.QtCore import (QCoreApplication, QByteArray, QDataStream, QThread,
	QIODevice)
from PyQt5.QtNetwork import QTcpServer, QTcpSocket
from time import sleep

class FortuneThread(QThread):
	"""docstring for FortuneThread"""
	def __init__(self, sockDescriptor, fortune, parent=None):
		super(FortuneThread, self).__init__(parent)
		self.sockDescriptor = sockDescriptor
		self.fortune = fortune
	
	def run(self):
		tcpSocket = QTcpSocket()
		tcpSocket.disconnected.connect(tcpSocket.deleteLater)
		if not tcpSocket.setSocketDescriptor(self.sockDescriptor):
			print('setSocketDescriptor error')
			return

		block = QByteArray()
		out = QDataStream(block, QIODevice.WriteOnly)
		#out.setVersion(QDataStream.Qt_4_0)
		s = self.fortune + '\n'
		out.writeRawData(s.encode('utf-8'))
		#out.writeQString(s)
		
		tcpSocket.write(block)
		#等待数据发送完成
		tcpSocket.waitForBytesWritten();
		tcpSocket.disconnectFromHost()
		tcpSocket.close()
		