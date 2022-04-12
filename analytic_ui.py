from data_flow_service import dataFlowService
import random
from datetime import datetime as dt
import time
import urwid

class analyticUI():
  def __init__(self):
    self.active_devices = []
    self.text_log = []
    layout = self.initUI()
    self.loop = urwid.MainLoop(layout, self.palette, event_loop=urwid.TwistedEventLoop())

  def getLoop(self):
    return self.loop

  def initUI(self):
    self.palette = [
      ('header', 'white,bold', ''),
      ('alarm', 'light red', ''),
      ('good', 'light green', ''),
      ('normal', '', '')
    ]
    self.stats_txt = urwid.Text(u"Statistics")
    self.log_txt = urwid.Text(u"log")
    top_filler = urwid.Filler(self.stats_txt, 'top')
    bot_filler = urwid.Filler(self.log_txt, 'top')
    log_header = urwid.Text(('header', 'LOG:'))
    bot_frame = urwid.Frame(header=log_header, body=bot_filler)
    layout = urwid.Pile([top_filler, bot_frame])
    return layout
    
  def removeDevice(self, device):
    if device in self.active_devices:
      self.active_devices.remove(device)

  def addDevice(self, device):
    if device not in self.active_devices:
      self.active_devices.append(device)

  def print(self, text, text_append=""):
    # Python program to demonstrate
    now = dt.now()
    date_str = now.strftime("%-d.%-m.%Y %-H:%M:%S: ")

    self.text_log.append(date_str+text+' '+str(text_append)+'\n')
    if len(self.text_log) > 10:
      self.text_log.pop(0)
    self.log_txt.set_text(self.text_log)
    self.loop.draw_screen()

  def printStats(self):
    header_text = []
    header_text.append(('header', 'Devices: \t'.expandtabs(5)))
    header_text.append(str(len(self.active_devices)))
    header_text.append('\n')
    header_text.append('\n')
    header_text.append(('header', 'Device id\t'.expandtabs(15)))
    header_text.append(('header', 'Inactive latest/limit\t'.expandtabs(25)))
    header_text.append(('header', 'Over active latest/limit'))
    i = 0
    for device in self.active_devices:
      header_text.append('\n')
      header_text = self.printDeviceStats(header_text, device)
      i += 1
      if i >= 10:
        break
    self.stats_txt.set_text(header_text)
    self.loop.draw_screen()

  def printDeviceStats(self, header_text, device):
    device_id = str(device.id)
    # In-Activity
    in_activity = device.dataservice.getInActivity()
    in_activity_limit = device.dataservice.getInActivityLimit()
    in_activity_status, in_activity_text = self.getActiveTexts(in_activity, in_activity_limit)
    in_activity_text += '\t'

    # Activity
    activity = device.dataservice.getActivity()
    activity_limit = device.dataservice.getActivityLimit()
    activity_status, activity_text = self.getActiveTexts(activity, activity_limit)

    header_text.append((device_id+'\t').expandtabs(15))
    header_text.append((in_activity_status, in_activity_text.expandtabs(25)))
    header_text.append((activity_status, activity_text))
    return header_text

  def getActiveTexts(self, activity, activity_limit):
    activity_status = 'normal'
    activity_text = 'Learning'
    if activity_limit:
      activity_text = str(activity)+'/'+str(activity_limit)
      activity_status = 'good'
      if activity > activity_limit:
        activity_status = 'alarm'
    return activity_status, activity_text

