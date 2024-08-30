//This program will be used with an Arduino Uno R4 with Matrix display to communicate in real time with python for drawing on the matrix display.
#include <Arduino_LED_Matrix.h>
ArduinoLEDMatrix matrix;
const uint32_t startup_frame[] = {0x30c79e7f, 0xe7fe3fc1, 0xf80f0060};
int size = 0;
byte bytes1[4];
byte bytes2[4];
byte bytes3[4];

void serial_wait(){
  while(Serial.available() < 4){
    //do nothing
  };
}

int combineBytes(byte data[4]){
  int dex = 0;
  int number = 0;
  while(dex < 4){
    number = number << 8;
    number += data[dex];
    dex++;
  };
  return number;
}

void setup(){
  Serial.begin(9600);
  matrix.begin();
  matrix.loadFrame(startup_frame);
}

void loop(){
  serial_wait();
  Serial.readBytes(bytes1, 4);
  int first_bytes = combineBytes(bytes1);
  serial_wait();
  Serial.readBytes(bytes2, 4);
  int second_bytes = combineBytes(bytes2);
  serial_wait();
  Serial.readBytes(bytes3, 4);
  int third_bytes = combineBytes(bytes3);
  uint32_t current_frame[] = {first_bytes, second_bytes, third_bytes};
  matrix.loadFrame(current_frame); 
}