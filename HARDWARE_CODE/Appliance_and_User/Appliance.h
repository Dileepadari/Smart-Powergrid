#ifndef _APPLIANCE_H
#define _APPLIANCE_H_
#include<Arduino.h>
#include "RelayModule.h"
enum AppPriority
{
   Low,
   Medium,
   Critical
};
enum HealthLevel
{
  Bad,
  Ok,
  Good
};
class Appliance
{
  private:
    RelayModule relaymod; 
    enum AppPriority priority;
    enum HealthLevel health;
    String appl_name;
    float base_current;
    float norm_temp;
  public:
    void create_appliance(enum AppPriority a_pri,String a_name,float base_curr,float t,int relay_pin);
};
#endif