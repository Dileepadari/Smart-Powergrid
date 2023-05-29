#ifndef __TempSensor_H_
#define __TempSensor_H_

#include <DHT.h>
#include <Arduino.h>
#define DHT11 11 

class DHTSensor {

private:
 
  DHT dht;
  int pin;

public:
  
  DHTSensor(int pin, int type) : dht(pin, type), pin(pin) { dht.begin();}
 
  

  float SenseTemperature();
};

#endif
