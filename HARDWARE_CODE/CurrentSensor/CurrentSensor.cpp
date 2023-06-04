#include "CurrentSensor.h"
CurrentSensor::CurrentSensor(int CurrentPin,int BasePin)
{
  inputPin=CurrentPin;
  basePin=BasePin;
}
  float CurrentSensor::updateBaseValue()
  {
    base_voltage=analogRead(basePin)*3.3/4095.0;
    return base_voltage;
  }
float CurrentSensor::getValueinA()
{
    float total_volts=0;
    updateBaseValue();
    for(int i=0;i<500;i++)
    {
       total_volts+=analogRead(inputPin)*3.3/4095.0;
       delay(12);
    }
    float avg_volts=total_volts/500.0;
    float curr_in_A=(avg_volts-base_voltage)*1000/185.0;
    Serial.println(avg_volts);
    if(curr_in_A<0)
    {
      return (curr_in_A*-1<0.15)?(0.0):(curr_in_A*-1);
    }
    else
    {
      return (curr_in_A<0.15)?(0.0):(curr_in_A);
    }
}
