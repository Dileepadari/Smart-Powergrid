#include<Arduino.h>
#include "CurrentSensor.h"
#ifndef HEALTH_H
#define HEALTH_H
class HealthMonitor
{
  private:
   int health_index;
  public:
   HealthMonitor(float base_curr);
   float base_current;
   int calculate_health(float current);
};
#endif