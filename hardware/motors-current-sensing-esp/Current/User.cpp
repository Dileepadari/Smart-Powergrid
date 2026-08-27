#include "User.h"
#include<PubSubClient.h>
#include<ThingSpeak.h>
User::User(String mqtt_username,String password,long channelID,String WriteKey,String ReadKey)
{
   Write_API_KEY=WriteKey;
   Read_API_KEY=ReadKey;
   mqttUsername=mqtt_username;
   clientID=mqtt_username;
   mqttPass=password;
   writeChannelID=channelID;
   mqttClient=PubSubClient(server,1883,wclient);  
}
void User::mqttConnect()
{
  mqttClient.connect(clientID.c_str(),mqttUsername.c_str(),mqttPass.c_str());
  while(!mqttClient.connected()){
     delay(2000);
     mqttClient.connect(clientID.c_str(),mqttUsername.c_str(),mqttPass.c_str()); 
     Serial.println("...");  
  }
  Serial.println("Connected");
}
void User::mqttPublish(float dataArray[],short fieldArray[])
{
  if(!mqttClient.connected())
  {
    mqttConnect();
  }
  String dataString="";
  for(int i=0;i<8;i++)
  {
    if(dataString!="")
    {
      dataString+="&";  
    }
    if(fieldArray[i]==0)
    {
      dataString+="field"+String(i+1)+="="+ThingSpeak.readStringField(writeChannelID,i+1,Read_API_KEY.c_str()); 
      delay(20);
      continue;
    }
    dataString+="field"+String(i+1)+"="+String(dataArray[i]);
  }
  String topicString="channels/"+String(writeChannelID)+"/publish";
  mqttClient.publish(topicString.c_str(),dataString.c_str());
  
  Serial.println(writeChannelID);
}