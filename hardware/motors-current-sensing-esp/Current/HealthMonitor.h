#include<Arduino.h>
#include "CurrentSensor.h"
#ifndef _HEALTH_H_
#define _HEALTH_H_
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
