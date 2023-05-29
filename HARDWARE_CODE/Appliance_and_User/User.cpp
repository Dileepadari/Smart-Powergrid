#include "User.h"
#include<PubSubClient.h>
#include<ThingSpeak.h>
User::User(String mqtt_username,String password,int channelID,String WriteKey)
{
   API_KEY=WriteKey;
   mqttUsername=mqtt_username;
   clientID=mqtt_username;
   mqttPass=password;
   writeChannelID=channelID;
   mqttClient=PubSubClient(server,1883,wclient);
}
void User::mqttPublish(float dataArray[],int fieldArray[])
{
  String dataString="field1="+String(dataArray[0]);
  String topicString="channels/"+String(writeChannelID)+"/publish";
  Serial.println(dataString);
  Serial.println(topicString);
  mqttClient.publish(topicString.c_str(),dataString.c_str());
  Serial.println(writeChannelID);
}