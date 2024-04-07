#include "HealthMonitor.h"
HealthMonitor::HealthMonitor(float base_curr)
{
  base_current=base_curr;
}
int HealthMonitor::calculate_health(float current)
{
    float change=abs(base_current-current)/base_current;
    health_index=3;
    if(change>0.05 &&  change<0.1)    {
      health_index=2;
    }
    else if(change>0.1)
    {
      health_index=1;
    }
    return health_index;
}