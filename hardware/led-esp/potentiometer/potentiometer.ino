#include <string.h>
#include<HTTPClient.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WebServer.h>
#include <ThingSpeak.h>
#include "time.h"
#include <WiFiClient.h>
#include <string>
#include <JSON.h>
#include <Arduino.h>
#include "RelayModule.h"
#include "CurrentSensor.h"
#include "User.h"
#include "HealthMonitor.h"



#define CSE_IP      "192.168.109.105"
#define CSE_PORT    5089
#define HTTPS     false
#define OM2M_ORGIN    "admin:admin"
#define OM2M_MN     "/~/in-cse/in-name/"
#define OM2M_AE     "Smart-Grid/" 
#define RES1_MOTOR_1  "Users/Resident1/Appliances/Motors/Motor_1"
#define RES1_MOTOR_2  "Users/Resident1/Appliances/Motors/Motor_2"
#define RES1_LED_1 "Users/Resident1/Appliances/LEDs/LED_1"
#define RES1_LED_2 "Users/Resident1/Appliances/LEDs/LED_2"
#define RES1_STAT1  "Users/Resident1/All_status"
#define RES2_MOTOR_1  "Users/Resident2/Appliances/Motors/Motor_1"
#define RES2_MOTOR_2  "Users/Resident2/Appliances/Motors/Motor_2"
#define RES2_LED_1 "Users/Resident2/Appliances/LEDs/LED_1"
#define RES2_STAT1  "Users/Resident2/All_status"

// RelayModule p32(32);

unsigned long user1_channel=2165368;
unsigned long user2_channel=2165370;
const char* ssid = "GALAXY KING";
const char* password = "DILEEPPRASANTHi";
#define ip1 34
#define ip2 35
WiFiClient client; 
HTTPClient http;

int User1LEDpriority;
int User1MOTORpriority;
int User2LEDpriority;
int User2MOTORpriority;

const char* server="http://smart-powergrid.000webhostapp.com/get_data.php";
const char* priorityserver="http://smart-powergrid.000webhostapp.com/priority.php";

#define led_ratedPower 0.09 
#define motor_ratedPower  1.7
#define buzzer_ratedPower 0.15  //NOTE: THESE VALUES ARE TAKEN FROM ONLINE SOURCES
#define power_source  5
#define led_res 90  //led resistence\
#define motor_res 585   //motor resistence
#define buzzer_res  1500000

float maxCurrent_led = 35;
float maxCurrent_motor = 100;
// float maxCurrent_buzzer = (buzzer_ratedPower/power_source)*0.9;

float minCurr_led=10;
float minCurr_motor=50;

HealthMonitor u1_L1_health(55.5);
HealthMonitor u1_L2_health(55.5);
HealthMonitor u2_L1_health(27.7777);


// RelayModule rm(26);
void setup() {
  Serial.begin(9600);
  // Serial.begin(115200);
  WiFi.begin(ssid,password);   
  while(WiFi.status()!=WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());   
  //  server.on("/",handleonconnect);    
  ThingSpeak.begin(client);
  pinMode(ip1, INPUT);
  pinMode(ip2, INPUT);
  // put your setup code here, to run once:
}
// 1 = toNO
// 0 = toNC
RelayModule p25(25);
RelayModule p26(26);
RelayModule p27(27);

String u1Status;
String u2Status;
float minCurrent_led = 10.0;
User user1("CzYeCTwuJTkIHg0GITswBSo","dLNq6KNxZKZA6tU8dm3uDnTV",user1_channel,"899FMRYW1H2FPCNJ","EFISS04IFA6364N9");
User user2("CzYeCTwuJTkIHg0GITswBSo","dLNq6KNxZKZA6tU8dm3uDnTV",user2_channel,"RLEHO8H1Z8C0I48Y","D3LNELVJ4YHFILVP");

String OM2M(String res) {
  http.begin("http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE + String() + res + "/la"); //Specify the URL
    http.addHeader("X-M2M-Origin", "guest:guest");
    http.addHeader("Accept", "application/json");
    int httpCode = http.GET();                                        //Make the request
    // String payload = ThingSpeak.readStringField(channel, field, readAPIKey.c_str()); 
    if (httpCode > 0) { //Check for the returning code
  
        String payload = http.getString();
        JSONVar payloade = JSON.parse(payload);
        Serial.println(httpCode);
        Serial.println("the payload is");
        payload = JSON.stringify(payloade["m2m:cin"]["con"]);
        payload.remove(0, 1);
        int len = payload.length();
        payload.remove(len-1, 1);
        Serial.println(payloade["m2m:cin"]["con"]);
        http.end();
        return payload;
      }
    
    else {
      Serial.println("Error on HTTP request");
    }
  
    http.end(); //Free the resources
}

void splitString(String s, String (&ans)[6]) {
  int ptr = 0;
  for (int i = 0; i < s.length(); i++) {
    String curr = "";
    while (i < s.length() && s[i] != ',') {
      curr += s[i++];
    }
    ans[ptr++] = curr;
  }
}

float u1Current1_LED = 0.0;
float u1Current2_LED = 0.0;
float u2Current_LED = 0.0;
float commonVoltage1 = 0.0;
float commonVoltage2 = 0.0;

void loop() {


    
  u1Status=ThingSpeak.readStringField(user1_channel, 6, "EFISS04IFA6364N9"); //(channelid, field number, read apikey)
  u2Status=ThingSpeak.readStringField(user2_channel, 7, "D3LNELVJ4YHFILVP"); //(channelid, field number, read apikey)


String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\"}";
  http.begin(priorityserver);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  if(httpResponseCode>0)
  {
    String payload = http.getString();
    User1LEDpriority = int( payload[1] - '0');
    User1MOTORpriority = int(payload[0]) - '0';
    

  }
  
    delay(500);

 jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\"}";
  http.begin(priorityserver);
  http.addHeader("Content-Type", "application/json");
   httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  if(httpResponseCode>0)
  {
    String payload = http.getString();
    User2LEDpriority = int( payload[1] - '0');
    User2MOTORpriority = int(payload[0] - '0');
    

  }
  
    delay(500);

  Serial.print("1) ");
  Serial.println(u1Status);
  Serial.print("2) ");
  Serial.println(u2Status);
//https://api.thingspeak.com/update?api_key=RLEH081Z8C0I48Y&field7=1,0,0:1,0,0:0,1,0:0,1,0
  u1Current1_LED = 0;
  u1Current2_LED = 0;
  u2Current_LED = 0;
  commonVoltage1 = 3.3 * analogRead(ip1) / 4095.0;
  commonVoltage2 = 3.3 * analogRead(ip2) / 4095.0;
  commonVoltage1 *= 1.5151515;
  commonVoltage2 *= 1.5151515;
  if (u1Status[12] == '0') {
    p25.commonToNO();
  } else if (u1Status[12] == '1') {
    u1Current1_LED = (commonVoltage1)/90.0;
    u1Current1_LED *= 1000;
    p25.commonToNC();
  }

  if (u1Status[18] == '0') {
    p26.commonToNO();
  } else if (u1Status[18] == '1') {
    u1Current2_LED = (commonVoltage1)/90.0;
    u1Current2_LED *= 1000;
    p26.commonToNC();
  }

  if (u2Status[12] == '0') {
    p27.commonToNO();
  } else if (u2Status[12] == '1') {
    u2Current_LED = (commonVoltage2)/180.0;
    u2Current_LED *= 1000;
    p27.commonToNC();
  }
  // short fieldArray1[8]={0,0,0,1,1,1,1,0};
  // short fieldArray2[8]={0,0,1,0,0,0,1,0};
  short fieldArray1[8]={1,1,1,1,1,1,1,1};
  short fieldArray2[8]={1,1,1,1,1,1,1,1};
  String om2mserver ="http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE;
  http.begin(om2mserver + String() + RES1_LED_1 + "/");
  Serial.println(om2mserver + String() + RES1_LED_1 + "/");
  http.addHeader("X-M2M-Origin", OM2M_ORGIN);
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("Content-Length", "100");
  // Serial.println(u1Status)  
  String send_data = String() + "{\"m2m:cin\": {"

  + "\"con\": \"" + "0.0" + "," + u1Status[12] + "," + String(u1Current1_LED) + "\","
  + "\"lbl\": \"data\""
  
  + "}}";
Serial.println(send_data);
int code = http.POST(send_data);
http.end();
Serial.println(code);
delay(100);

om2mserver ="http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE;
  http.begin(om2mserver + String() + RES1_LED_2 + "/");
  Serial.println(om2mserver + String() + RES1_LED_2 + "/");
  http.addHeader("X-M2M-Origin", OM2M_ORGIN);
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("Content-Length", "100");
  send_data = String() + "{\"m2m:cin\": {"

  + "\"con\": \"" + "0.0" + "," + u1Status[18] + "," + String(u1Current2_LED) + "\","

  + "\"lbl\": \"data\""
  
  + "}}";
Serial.println(send_data);
code = http.POST(send_data);
http.end();
Serial.println(code);
delay(100);

om2mserver ="http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE;
  http.begin(om2mserver + String() + RES2_LED_1 + "/");
  Serial.println(om2mserver + String() + RES2_LED_1 + "/");
  http.addHeader("X-M2M-Origin", OM2M_ORGIN);
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("Content-Length", "100");
  send_data = String() + "{\"m2m:cin\": {"

  + "\"con\": \"" + "0.0" + "," + u2Status[12] + "," + String(u2Current_LED) + "\","

  + "\"lbl\": \"data\""
  
  + "}}";
Serial.println(send_data);
code = http.POST(send_data);
http.end();
Serial.println(code);
delay(100);


// http.begin("http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE + String() + RES1_STAT1 + "/la"); //Specify the URL
//     http.addHeader("X-M2M-Origin", "guest:guest");
//     http.addHeader("Accept", "application/json");
//     int httpCode = http.GET();                                        //Make the request
//     String payload = ThingSpeak.readStringField(user1_channel, 6, user1.Read_API_KEY.c_str()); // chg
//     if (httpCode > 0) { //Check for the returning code
  
//         payload = http.getString();
//         JSONVar payloade = JSON.parse(payload);
//         Serial.println(httpCode);
//         Serial.println("the payload is");
//         payload = JSON.stringify(payloade["m2m:cin"]["con"]);
//         payload.remove(0, 1);
//         int len = payload.length();
//         payload.remove(len-1, 1);
//         Serial.println(payloade["m2m:cin"]["con"]);
        
//       }
    
//     else {
//       Serial.println("Error on HTTP request");
//     }
  
//     http.end(); //Free the resources
  // status;temperature;current;speed;direction

  String result1 = OM2M(RES1_MOTOR_1);
  String result2 = OM2M(RES1_MOTOR_2);
  String result1Split[6];
  String result2Split[6];
  splitString(result1, result1Split);
  splitString(result2, result2Split);
  Serial.printf("result1: %s\n", result1);
  Serial.println("Debug begin");
  for (auto i : result1Split) {
    Serial.printf("[DEBUG]: %s\n", i);
  }
  Serial.println("Debug end");
  String curr1 =  result1Split[2];// result1 current
  String curr2 =  result2Split[2];  // result2 current
  String temp1 =  result2Split[1]; // result2 temperature
  String heal_res1_mot1 = result1Split[5];
  String heal_res1_mot2 = result2Split[5];
  int healths[2] = {u1Current1_LED>0?u1_L1_health.calculate_health(u1Current1_LED):healths[0],u1Current2_LED>0? u1_L2_health.calculate_health(u1Current2_LED):healths[1]};
  String health = heal_res1_mot1+","+heal_res1_mot2+","+ String(healths[0]) + "," + String(healths[1]);
  Serial.printf("Health: %s\n", health);
  String dataArray1[8]={curr1,temp1,curr2,String(u1Current1_LED),String(u1Current2_LED),OM2M(RES1_STAT1),health,"0"};
  user1.mqttPublish(dataArray1,fieldArray1);  


    http.begin("http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE + String() + RES2_STAT1 + "/la"); //Specify the URL
    http.addHeader("X-M2M-Origin", "guest:guest");
    http.addHeader("Accept", "application/json");
    int httpCode = http.GET();                                        //Make the request
    String payload = ThingSpeak.readStringField(user2_channel, 7, user2.Read_API_KEY.c_str());
    if (httpCode > 0) { //Check for the returning code
  
        payload = http.getString();
        JSONVar payloade = JSON.parse(payload);
        Serial.println(httpCode);
        Serial.println("the payload is");
        payload = JSON.stringify(payloade["m2m:cin"]["con"]);
        payload.remove(0, 1);
        int len = payload.length();
        payload.remove(len-1, 1);
        Serial.println(payloade["m2m:cin"]["con"]);
        
      }
  
    else {
      Serial.println("Error on HTTP request");
    }
  
    http.end(); //Free the resources
  Serial.printf("commonVoltage1: %f\n", commonVoltage1);
  Serial.printf("commonVoltage2: %f\n", commonVoltage2);
  Serial.printf("u1Current1: %f\n", u1Current1_LED);
  Serial.printf("u1Current2: %f\n", u1Current2_LED);
  Serial.printf("u2Current: %f\n", u2Current_LED);
  Serial.printf("user1LEDPriority: %d\n", User1LEDpriority);
  Serial.printf("user2LEDPriority: %d\n", User2LEDpriority);
  
  result1 = OM2M(RES2_MOTOR_1);
  result2 = OM2M(RES2_MOTOR_2);
  splitString(result1, result1Split);
  splitString(result2, result2Split);
  curr1 = result1Split[2];
  curr2 = result2Split[2];
  String heal_res2_mot1 = result1Split[5];
  String heal_res2_mot2 = result2Split[5];
  int healths2[1] = {u2Current_LED>0?u2_L1_health.calculate_health(u2Current_LED):healths2[0]};
  health = heal_res2_mot1+","+heal_res2_mot2+","+ String(healths2[0]) + "," + "0";
  Serial.printf("Health2: %s\n", health);  
  String dataArray2[8]={curr1, curr2,String(u2Current_LED),"40.0","0","0",payload,health};
  user2.mqttPublish(dataArray2,fieldArray2);


if(u1Status[12]=='1' && u1Current1_LED==0){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Wire is down for LED1!");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Wire is down for LED1!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
if(u1Status[12]=='0' && u1Current1_LED==1){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Unathorised Current is Drawn at LED1!");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Unathorised Current is Drawn at LED1!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }

if(u1Status[18]=='1' && u1Current2_LED==0){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Wire is down for LED2!");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Wire is down for LED2!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  if(u1Status[18]=='0' && u1Current2_LED==1){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Unathorised Current is Drawn at LED2!");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Unathorised Current is Drawn at LED2!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  if(u2Status[12]=='1' && u2Current_LED==0){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Wire is down for LED!");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Wire is down for LED!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  if(u2Status[12]=='0' && u2Current_LED==1){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Unathorised Current is Drawn at LED!");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Unathorised Current is Drawn at LED!\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }

if(User1LEDpriority==1){
if(u1Current1_LED >maxCurrent_led || u1Current2_LED > maxCurrent_led){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Increase resistance for LEDs Potentiometer");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Increase resistance for LEDs Potentiometer\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  
  if ((u1Status[12]=='1' && u1Current1_LED < 28) || (u1Status[18]=='1' && u1Current2_LED < 28)){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Decrase resistance for LEDs Potentiometer");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Decrease resistance for LEDs Potentiometer\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  }

if(User2LEDpriority==1){
if(u2Current_LED > 24){
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Increase resistance for LEDs Potentiometer");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Increase resistance for LEDs Potentiometer\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  
  if (u2Status[12]=='1' && u2Current_LED < 18) {
    // Error[0][1] = "u2m2 taking power when off";
    Serial.println("Decrase resistance for LEDs Potentiometer");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Decrease resistance for LEDs Potentiometer\",\"appliance\":\"LEDs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  }

}
//OM2M IMPLEMENTATION
// //
// RelayModule u1m1(33);
// RelayModule u1m2(32);
// RelayModule u2m1(26);
// RelayModule u2m2(14);
// // RelayModule p32(32);
// CurrentSensor u1m1Sensor(0, 0, Motor, ON);
// CurrentSensor u1m2Sensor(0, 0, Motor, ON);
// CurrentSensor u2m1Sensor(0, 0, Motor, ON);
// CurrentSensor u2m2Sensor(0, 0, Motor, ON);


//User user1("CzYeCTwuJTkIHg0GITswBSo","dLNq6KNxZKZA6tU8dm3uDnTV",user1_channel,"899FMRYW1H2FPCNJ");
//PubSubClient mqttClient(server,18/83,client)