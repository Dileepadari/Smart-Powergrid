#include "Appliance.h"
void Appliance::create_appliance(enum AppPriority a_pri,String a_name,float base_curr,float t,int relay_pin)
{
    priority=a_pri;
    appl_name=a_name;
    base_current=base_curr;
    norm_temp=t;
    health=Good;
    relaymod=RelayModule(relay_pin);
}