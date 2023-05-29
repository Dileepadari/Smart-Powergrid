#include "TempSensor.h"
#include <DHT.h>
#include "User.h"
#include <PubSubClient.h>
#include <ThingSpeak.h>
#include "WiFi.h"

char* ssid = "zzz";
char* passwd="yyy";

int Channel_ID_1 = 2165368;
int Channel_ID_2 = 2165370;

String API_key1 = "899FMRYW1H2FPCNJ";
String API_key2 = "RLEHO8H1Z8C0I48Y";
int Field_1 = 2;
int Field_2_1 = 4;
int Field_2_2 = 6;

String Client_ID = "CzYeCTwuJTkIHg0GITswBSo";
String mqttPass = "CzYeCTwuJTkIHg0GITswBSo";
String mqttUser = "dLNq6KNxZKZA6tU8dm3uDnTV";

WiFiClient client;
PubSubClient mqttClient(client);

User user1(mqttUser, mqttPass,Channel_ID_1, API_key1);  
User user2(mqttUser, mqttPass,Channel_ID_2, API_key2);  

DHTSensor sensors[] = { DHTSensor(25,11), DHTSensor(26,11), DHTSensor(27,11) };

void setup() {
  Serial.begin(115200);
  
}

void loop() 
{
   float temp_array[3];
   for (int i = 0; i < 3; i++) 
  {
     temp_array[i]=sensors[i].SenseTemperature();
     float temp[]={temp_array[i]};
     if(i==0)
     {
        int fieldarray[] = {0,1,0,0,0,0,0,0};
        user1.mqttPublish(temp, fieldarray);
     }
     if(i==1)
     {
        int fieldarray[] = {0,0,0,1,0,0,0,0};
        user2.mqttPublish(temp, fieldarray);
     }
     if(i==2)
     {
        int fieldarray[] = {0,0,0,0,0,1,0,0};
        user2.mqttPublish(temp, fieldarray);
     }
  }

  delay(2000);
}
