#ifndef CurrentSensor_H_
#define CurrentSensor_H_
#include<Arduino.h>
class CurrentSensor
{
  private:
    int inputPin;
    int basePin;
    float base_voltage;
  public:
    CurrentSensor(int CurrentPin,int BasePin);
    float getValueinA();
    float updateBaseValue();
};
#endif