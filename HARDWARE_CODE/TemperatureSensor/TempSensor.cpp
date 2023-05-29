#include "TempSensor.h"

float DHTSensor::SenseTemperature()
{
    float temperature = dht.readTemperature();
    return temperature;
}
