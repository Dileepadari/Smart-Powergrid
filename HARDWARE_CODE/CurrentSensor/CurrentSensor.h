#ifndef CurrentSensor_H_
#define CurrentSensor_H_
#include<Arduino.h>
class CurrentSensor
{
  private:
    int inputPin;
    float base_voltage;
    char* APIKey;
  public:
    CurrentSensor(int CurrentPin);
    float getBaseValue(int base_pin);
    float getValueinA();
};
#endif
