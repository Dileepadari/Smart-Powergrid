#ifndef CurrentSensor_H_
#define CurrentSensor_H_
#include<Arduino.h>
class CurrentSensor
{
  private:
    int inputPin;
  public:
    CurrentSensor(int CurrentPin);
    float getValueinmA();
};
#endif