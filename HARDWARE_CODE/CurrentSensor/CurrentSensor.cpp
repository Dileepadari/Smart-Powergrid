#include "CurrentSensor.h"
CurrentSensor::CurrentSensor(int CurrentPin)
{
  inputPin=CurrentPin;
}
float CurrentSensor::getBaseValue(int base_pin)
{
   base_voltage=analogRead(base_pin)*3.3/4095.0;
   return base_voltage;
}
float CurrentSensor::getValueinA()
{
  float volts=analogRead(inputPin)*3.3/4095.0;
  Serial.println(volts);
  float curr_in_A=(volts-base_voltage)*1000/185.0;
  if(curr_in_A<0)
  {
    return curr_in_A*-1;
  }
  else
  {
    return curr_in_A;
  }
}
