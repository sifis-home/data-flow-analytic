from twisted.internet.protocol import Factory
from twisted.internet import reactor

#import logging

from analytic_ui import analyticUI
from analytic_device import analyticDevice

import parameters as param

#logging.getLogger('twisted').setLevel(logging.CRITICAL)

class analyticServer(Factory):
  def __init__(self, ui_class):
    self.clients = {}
    self.id = {"last_id": 0}
    self.ui_class = ui_class
    reactor.callLater(0.5, self.asyncCall)

  # Runs when client connects
  def buildProtocol(self, addr):
    return analyticDevice(self.clients, self.ui_class, self.id)

  # Run every half second to update UI
  def asyncCall(self):
    self.ui_class.printStats()
    reactor.callLater(0.5, self.asyncCall)

# Create UI
ui_class = analyticUI()
# Get event loop from UI
loop = ui_class.getLoop()
# Run server
reactor.listenTCP(param.server_port, analyticServer(ui_class))
# Start event loop
loop.run()