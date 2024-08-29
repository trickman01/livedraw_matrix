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

void setup(){
  Serial.begin(9600);
  matrix.begin();
  matrix.loadFrame(startup_frame);
}

void loop(){
  serial_wait();
  Serial.readBytes(bytes1, 4);
  int dex = 0;
  int first_byte = 0;
  while(dex < 4){
    if(dex > 0){
      first_byte = first_byte << 8;
    }
    first_byte = first_byte | bytes1[dex];
    dex++;
  }
  serial_wait();
  Serial.readBytes(bytes2, 4);
  dex = 0;
  int second_byte = 0;
  while(dex < 4){
    if(dex > 0){
      second_byte = second_byte << 8;
    }
    second_byte = second_byte | bytes2[dex];
    dex++;
  }
  serial_wait();
  Serial.readBytes(bytes3, 4);
  dex = 0;
  int third_byte = 0;
  while(dex < 4){
    if(dex > 0){
      third_byte = third_byte << 8;
    }
    third_byte = third_byte | bytes3[dex];
    dex++;
  }
  uint32_t current_frame[] = {first_byte, second_byte, third_byte};
  matrix.loadFrame(current_frame);




    
}