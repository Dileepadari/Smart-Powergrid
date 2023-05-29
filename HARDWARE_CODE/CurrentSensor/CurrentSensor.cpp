#include "CurrentSensor.h"
CurrentSensor::CurrentSensor(int CurrentPin)
{
  inputPin=CurrentPin;
}
float CurrentSensor::getValueinA()
{
  float volts=analogRead(inputPin)/1200.0;
  Serial.println(volts);
  float curr_in_A=(volts-2.5)*1000/185.0;
  if(curr_in_A<0)
  {
    return curr_in_A*-1;
  }
  else
  {
    return curr_in_A;
  }
}