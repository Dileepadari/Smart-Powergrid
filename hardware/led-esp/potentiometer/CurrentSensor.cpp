#include "CurrentSensor.h"
/*
50mA -> for LEDS
100mA -> for motors
80 mA -> for med
60ma -> for low
*/
CurrentSensor::CurrentSensor(int CurrentPin,int BasePin,ApplianceType AType,ApplianceStatus init_status)
{
  inputPin=CurrentPin;
  basePin=BasePin;
  AppType=AType;
  initial_status=init_status;
}
float CurrentSensor::updateBaseValue()
{
    base_voltage=analogRead(basePin)*3.3/4095.0;
    return base_voltage;
}
double randomDouble(double minf, double maxf)
{
  return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31);  // use 1ULL<<63 for max double values)
}
float CurrentSensor::getValueinmA()
{
    float total_curr=0;
    if (initial_status == OFF) {
      return 0.0;
    } 
    if(AppType==LED)
    {
      for(int i=0;i<500;i++)
      {
        total_curr+=randomDouble(46.81,54.05);
      }
      return total_curr/500.0;
    }
    else
    {
      float lower, upper;
      if (initial_status == LO) {
        lower = 53.45;
        upper = 64.39;
      } else if (initial_status == MEDIUM) {
        lower = 73.28;
        upper = 86.12;
      } else {
        lower = 89.92;
        upper = 107.01;
      }
      for(int i=0;i<500;i++)
      {
        total_curr+=randomDouble(lower,upper);
      }
      return total_curr/500.0;
    }
    // float total_volts=0;
    // updateBaseValue();
    // for(int i=0;i<500;i++)
    // {
    //    total_volts+=analogRead(inputPin)*3.3/4095.0;
    //    delay(12);
    // }
    // float avg_volts=total_volts/500.0;
    // float curr_in_A=(avg_volts-base_voltage)*1000/185.0;
    // Serial.print("Avg voltage: ");
    // Serial.println(avg_volts);
    // Serial.print("Avg current: ");
    // Serial.println(curr_in_A);
    // if(curr_in_A<0)
    // {
    //   return (curr_in_A*-1<0.15)?(0.0):(curr_in_A*-1);
    // }
    // else
    // {
    //   return (curr_in_A<0.15)?(0.0):(curr_in_A);
    // }
}
