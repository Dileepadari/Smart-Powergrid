#ifndef _USER_H_
#define _USER_H_
#include<Arduino.h>
#include<PubSubClient.h>
#include<ThingSpeak.h>
#include<WiFi.h>
class User
{
  private:
    String API_KEY;
    const char* server="mqtt3.thingspeak.com";
    String mqttUsername;
    String clientID;
    String mqttPass;
    int writeChannelID;
    WiFiClient wclient;
    PubSubClient mqttClient;
  public:
    User(String mqtt_username,String password,int channelID,String WriteKey);
    void mqttPublish(float dataArray[],int fieldArray[]);
};
#endif