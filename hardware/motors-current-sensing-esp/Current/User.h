#ifndef _USER_H_
#define _USER_H_
#include<Arduino.h>
#include<PubSubClient.h>
#include<ThingSpeak.h>
#include<WiFi.h>
class User
{
  private:
    String Read_API_KEY;
    String Write_API_KEY;
    const char* server="mqtt3.thingspeak.com";
    String mqttUsername;
    String clientID;
    String mqttPass;
    long writeChannelID;
    WiFiClient wclient;
    PubSubClient mqttClient;
    String field_names[8];
    void mqttConnect();
  public:
    User(String mqtt_username,String password,long channelID,String WriteKey,String ReadKey);
    void mqttPublish(float dataArray[],short fieldArray[]);
};
#endif