from twisted.protocols.basic import LineReceiver
from twisted.protocols.policies import TimeoutMixin

from data_flow_service import dataFlowService

import parameters as param

class analyticDevice(LineReceiver, TimeoutMixin):
  delimiter = b"\n"  # unix terminal style newlines. remove this line

  def __init__(self, clients, ui_class, id_list):
    self.clients = clients
    self.id = id_list["last_id"] + 1
    id_list["last_id"] += 1
    self.ui_class = ui_class
    self.dataservice = dataFlowService(param.data_flow_buffer_size, param.data_flow_byterate_time)

  # Twisted TCP function: called when device connects to server
  def connectionMade(self):
    self.ui_class.print("Connected from", self.transport.client)
    self.clients[self.id] = self
    self.ui_class.addDevice(self)

  # Twisted TCP function: called when device loses a connection
  def connectionLost(self, reason):
    self.ui_class.print("Disconnected from ", self.transport.client)
    self.closeConnection()
  
  # Twisted TCP function: This actually closes the connection
  def closeConnection(self):
    # Remove instance from clients
    if self.id in self.clients:
      self.ui_class.print("Delete device %s from clients list" % (self.id))
      del self.clients[self.id]
    self.ui_class.removeDevice(self)

  # Twisted TCP function: called when data is received
  def lineReceived(self, line):
    self.ui_class.print("Line from device: "+str(self.id))
    self.dataservice.push(len(line))