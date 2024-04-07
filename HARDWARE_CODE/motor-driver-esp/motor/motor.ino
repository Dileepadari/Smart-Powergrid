#include <string.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ThingSpeak.h>
#include <WiFiClient.h>
// #include "RelayModule.h"
#include "motor.h"

unsigned long user1_channel=2165368;
unsigned long user2_channel=2165370;
const char* ssid = "Lorem ipsum";
const char* password = "Getlostyoutrespassers";



WiFiClient client; 
WebServer server(80);   

Motor m1("resident1",23,22,21,19,0);
Motor m2("resident2",2,15,4,5,1);

// RelayModule p32(32);

void setup()
{
//  pinMode(D2,OUTPUT);
//  digitalWrite(D2,0);
  
 Serial.begin(115200);
 WiFi.setHostname("MotorDriverESP");
 WiFi.begin(ssid,password);   
 while(WiFi.status()!=WL_CONNECTED)
 {
   delay(500);
   Serial.print(".");
 }
 Serial.println(WiFi.localIP());   
//  server.on("/",handleonconnect);    
 ThingSpeak.begin(client);      
//  server.begin();   

  m1.Setup();
  m2.Setup();
  
  m1.TurnOn();
  m2.TurnOn();
}

String u1Status, u2Status;



void loop()
{
//  server.handleClient();   
 u1Status=ThingSpeak.readStringField(user1_channel, 6, "EFISS04IFA6364N9"); //(channelid, field number, read apikey)
 u2Status=ThingSpeak.readStringField(user2_channel, 7, "D3LNELVJ4YHFILVP"); //(channelid, field number, read apikey)
 Serial.println(ThingSpeak.getLastReadStatus());
 Serial.print("1) ");
 Serial.println(u1Status);
 Serial.print("2) ");
 Serial.println(u2Status);
  
  if(u1Status[2]=='0'){
    m1.SetSpeed(0);
  }
  else if(u1Status[2]=='1'){
    m1.SetSpeed(1);
  }
  else if(u1Status[2]=='2'){
    m1.SetSpeed(2);
  }

  if(u1Status[4]=='0'){
    m1.SetDirection(0);
  }
  else if(u1Status[4]=='1'){
    m1.SetDirection(1);
  }

  // if(u1Status[2]=='0'){
  //   m1.SetSpeed(0);
  // }
  // else if(u1Status[2]=='1'){
  //   m1.SetSpeed(1);
  // }
  // else if(u1Status[2]=='2'){
  //   m1.SetSpeed(2);
  // }

  // if(u1Status[4]=='0'){
  //   u1m2.SetDirection(0);
  // }
  // else if(u1Status[4]=='1'){
  //   u1m2.SetDirection(1);
  // }



  if(u2Status[2]=='0'){
    m2.SetSpeed(0);
  }
  else if(u2Status[2]=='1'){
    m2.SetSpeed(1);
  }
  else if(u2Status[2]=='2'){
    m2.SetSpeed(2);
  }

  if(u2Status[4]=='0'){
    m2.SetDirection(0);
  }
  else if(u2Status[4]=='1'){
    m2.SetDirection(1);
  }

//https://api.thingspeak.com/update?api_key=RLEH081Z8C0I48Y&field7=1,0,0:1,0,0:0,1,0:0,1,0

 
 delay(1000);
}

