#include <string.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ThingSpeak.h>
#include <WiFiClient.h>
#include "RelayModule.h"

unsigned long user1_channel=2165368;
unsigned long user2_channel=2165370;
const char* ssid = "Lorem ipsum";
const char* password = "Getlostyoutrespassers";

unsigned int value;
// #define D2 2

WiFiClient client;  
WebServer server(80);   


RelayModule u1m1(33);
RelayModule u1m2(32);
RelayModule u2m1(26);
RelayModule u2m2(14);
// RelayModule p32(32);

void setup()
{
//  pinMode(D2,OUTPUT);
//  digitalWrite(D2,0);
  
 Serial.begin(115200);
 WiFi.setHostname("Motor Relays");
 WiFi.begin(ssid,password);   
 while(WiFi.status()!=WL_CONNECTED)
 {
   delay(500);
   Serial.print(".");
 }
 Serial.println(WiFi.localIP());   
//  server.on("/",handleonconnect);    
 ThingSpeak.begin(client); 
 Serial.println("thingspeak");     
//  server.begin();   
}

String u1Status, u2Status;



void loop()
{
//  server.handleClient();   
 u1Status=ThingSpeak.readStringField(user1_channel, 6, "EFISS04IFA6364N9"); //(channelid, field number, read apikey)
 u2Status=ThingSpeak.readStringField(user2_channel, 7, "D3LNELVJ4YHFILVP"); //(channelid, field number, read apikey)
 int statusCode = ThingSpeak.getLastReadStatus();
  Serial.println(statusCode);
 Serial.print("1) ");
 Serial.println(u1Status);
 Serial.print("2) ");
 Serial.println(u2Status);
  
  if(u1Status[0]=='0'){
    u1m1.commonToNO();
  }
  else if(u1Status[0]=='1'){
    u1m1.commonToNC();
  }

  if(u1Status[6]=='0'){
    u1m2.commonToNC();
  } else if(u1Status[6]=='1'){
    u1m2.commonToNO();
  }

  if(u2Status[0]=='0'){
    u2m1.commonToNO();
  }
  else if(u2Status[0]=='1'){
    u2m1.commonToNC();
  }

  if(u2Status[6]=='0'){
    u2m2.commonToNO();
  }
  else if(u2Status[6]=='1'){
    u2m2.commonToNC();
  }

//https://api.thingspeak.com/update?api_key=RLEH081Z8C0I48Y&field7=1,0,0:1,0,0:0,1,0:0,1,0

 
 delay(1000);
}