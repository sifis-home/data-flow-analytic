# Data Flow Analytic

The aim of this analytic is to detect if there is a change in the device network data flow. This analytic will notice if the device gets overactive or inactive suddenly.

The analytic is based on statistical method called Interquartile range (IQR). Algorithm stores data parameter to fixed size array and runs analytic over that array. Array size must be adjusted accoring to application. If array size is big algorithm uses more memory and analytic speed is a bit slower but detection speed is not affected. In case of small array less resources are used but algorithm can give more false alarms.

Stored parameters are data length in bytes (2 bytes), data time (8 bytes) in 0.1 second accuracy, time difference to previous packet (4 bytes) in 0.1 second accuracy and calculated byterate (4 bytes). Totally one entry takes 18 bytes of memory and if array size has been set to 1000 then analytics in one device will be using 18 kB memory. Analytic parameters can be adjusted in **parameters.py** file.

The time used to calculate byterate is also adjustable. If byterate time is small and device sends packets with big intervals then byterate is same as packet size. When byterate time is big algorithm allows short time and high datarate databursts.

Analytic triggers overactive alarm when byterate gets too high and inactive alarm is triggered when time difference between data packets gets too high.

This analytic uses pyhton3 and requires following libraries:
- numpy
- twisted
- urwid

## Files in this directory are as below:
- **"parameters.py"**: Set analytic parameters
- **"analytic_server.py"**: Server to receive data flow to be analyzed
- **"analytic_device.py"**: Class for single device
- **"analytic_ui.py"**: User interface for the analytic
- **"data_flow_service.py"**: The analytic algorithm
- **"data_client.py"**: Client to produce random data