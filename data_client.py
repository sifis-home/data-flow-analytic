from twisted.internet import stdio, reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.basic import LineReceiver

import random

import parameters as param

class analyticClient(Protocol):
  def __init__(self):
    self.interval = 1
    self.connected = False
    reactor.callLater(0.1, self.checkConnection)

  def connectionMade(self):
    print("Connected to server")
    self.connected = True
    stdio.StandardIO(keyboardUI(self))
    reactor.callLater(1, self.sendMessage)

  def checkConnection(self):
    if not self.connected:
      print("Could not connect to server")
      reactor.stop()

  def sendMessage(self):
    prefix = b"Temp: "
    payload = random.randint(180, 240)
    self.transport.write(prefix+str(payload).encode()+b"\n")
    reactor.callLater(self.getInterval(), self.sendMessage)

  def getInterval(self):
    # None is random
    if self.interval is None:
      return random.randint(1, 50) / 5
    if self.interval == 0:
      return 10
    interval = random.randint(self.interval*10-4, self.interval*10+4)
    return interval / 5

  def setInterval(self, interval):
    self.interval = interval

  def connectionLost(self, reason):
    print("Quit")
    reactor.stop()

class keyboardUI(LineReceiver):
  delimiter = b"\n"  # unix terminal style newlines. remove this line

  def __init__(self, tcp_connection):
    self.tcp_connection = tcp_connection

  def connectionMade(self):
    self.sendLine(b"Client console. Commands are: 'r' for random, '0' for no data or any number 1-5 to set sending speed. Press enter after command")

  def lineReceived(self, line):
    # Ignore blank lines
    if not line:
      return
    line = line.decode("ascii")
    if not line.isnumeric():
      if line == 'q':
        self.tcp_connection.transport.loseConnection()
      if line == 'r':
        self.sendLine(b"Set interval to random")
        self.tcp_connection.setInterval(None)
      return
    in_num = int(line)
    if in_num >= 0 and in_num <= 5:
      self.sendLine(b"Set interval to: "+str(in_num).encode())
      self.tcp_connection.setInterval(in_num)

point = TCP4ClientEndpoint(reactor, "localhost", param.server_port)
tcp_connection = connectProtocol(point, analyticClient())

reactor.run()