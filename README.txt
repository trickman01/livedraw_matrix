Use of these programs will allow you to draw a matrix in python and the matrix of the Arduino Uno R4 Wifi will update.  Designed to be used for drawing test patterns in real-time.

In the python program:
SPACEBAR will output a 3 hex code for the current matrix on the arduino
'R' key will reset all LEDs in the matrix to the off state
'F' will turn on all LEDs in the matrix
'U' will push data to the Arduino board manually.  Shouldn't need to use this, but could be useful if you disconnect and reconnect your Arduino while the program is running.

In the Arduino sketch:
Simply compile the sketch onto your Arduino Uno R4 Wifi board and note the COM port using.  Add the COM port to the config file where noted.