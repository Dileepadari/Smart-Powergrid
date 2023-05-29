#ifndef CurrentSensor_H_
#define CurrentSensor_H_
#include<Arduino.h>
class CurrentSensor
{
  private:
    int inputPin;
    char* APIKey;
  public:
    CurrentSensor(int CurrentPin);
    float getValueinA();
};
#endif