import numpy as np
import time

class dataFlowService():
  # buffer_size is FIFO buffer size to constantly analyze based on history
  # byterate_time is time in seconds to calculate byterate
  def __init__(self, buffer_size, byterate_time):
    dt = np.dtype([('length', np.uint16), ('time', np.uint64), ('time_diff', np.uint32), ('byterate', np.uint32)])
    self.data = np.zeros(buffer_size, dtype=dt)
    self.last_time = None
    self.buffer_size = buffer_size
    self.byterate_time = byterate_time
    self.last_point = -1
    self.full_buffer = False
    self.byterate_limit = None
    self.time_limit = None


  def push(self, data_len, data_time = None):
    if not data_time:
      data_time = int(time.time()*10)
    self.last_point += 1
    if self.last_point >= self.buffer_size:
      self.last_point = 0
      self.full_buffer = True
    self.data[self.last_point]['length'] = data_len
    self.data[self.last_point]['time'] = data_time
    if self.last_time != None:
      self.data[self.last_point]['time_diff'] = data_time - self.last_time
      self.setByterate()
    if self.full_buffer:
      self.analyze()
    self.last_time = data_time

  def analyze(self):
    # Add timeout for too long
    self.analyzeLow()
    self.analyzeHigh()

  # Alert if device is inactive
  def analyzeLow(self):
    high_limit = self.getIQR('time_diff')
    self.time_limit = high_limit

  # Alert if device is too active
  def analyzeHigh(self):
    high_limit = self.getIQR('byterate')
    self.byterate_limit = high_limit

  def getIQR(self, column):
    Q1,Q3 = np.percentile(self.data[column], [25, 75])
    IQR = Q3 - Q1
    #lower_range = Q1 - (1.5 * IQR)
    high_limit = Q3 + (1.5 * IQR)
    return high_limit

  def setByterate(self):
    # Calculate byterate_time from latest point
    from_time = self.data[self.last_point]['time']-self.byterate_time
    # Get byterate sum
    byte_sum = np.sum(self.data['length'], where=self.data['time'] > from_time)
    # Set byterate sum to data
    self.data[self.last_point]["byterate"] = byte_sum

  def getActivity(self):
    return self.data[self.last_point]["byterate"]

  def getActivityLimit(self):
    return self.byterate_limit

  def getInActivity(self):
    if self.last_time != None:
      return (int(time.time()*10)-self.last_time)/10
    return 0

  def getInActivityLimit(self):
    if self.time_limit:
      return self.time_limit/10
    return None

  def isTooActive(self):
    if self.byterate_limit:
      return self.data[self.last_point]["byterate"] > self.byterate_limit
    return False

  def whenTooInActive(self):
    if self.time_limit:
      time_to_inactive = self.last_time + self.time_limit - int(time.time()*10)
      if time_to_inactive < 0:
        return 0
      return time_to_inactive
    return 0
