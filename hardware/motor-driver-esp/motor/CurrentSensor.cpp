#include "CurrentSensor.h"
CurrentSensor::CurrentSensor(int CurrentPin)
{
  inputPin=CurrentPin;
}
float CurrentSensor::getValueinmA()
{
    float total_curr=0;
    float volt;
    for(int i=0;i<500;i++)
    {
       volt=analogRead(CurrentPin)*3.3/4095.0;
       total_curr += (volt - 2.5) / 0.185;
    }
    return total_curr*2.0;
}
