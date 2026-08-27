#ifndef CurrentSensor_H_
#define CurrentSensor_H_
#include<Arduino.h>
typedef enum ApplianceType
{
  LED,
  Motor
} ApplianceType;
typedef enum ApplianceStatus
{
  ON,
  OFF,
  HI,
  MEDIUM,
  LO
} ApplianceStatus;
class CurrentSensor
{
  private:
    int inputPin;
    int basePin;
    float base_voltage;
    ApplianceType AppType;
  public:
    ApplianceStatus initial_status;
    CurrentSensor(int CurrentPin,int BasePin,ApplianceType AType,ApplianceStatus init_status);
    float getValueinmA();
    float updateBaseValue();
};
#endif