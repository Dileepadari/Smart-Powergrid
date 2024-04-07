#include "CurrentSensor.h"
// #include "TempSensor.h"
// #include <DHT.h>
#include "User.h"
#include <PubSubClient.h>
#include <ThingSpeak.h>
#include "WiFi.h"
#include <WiFiClient.h>
#include <HTTPClient.h>
#include "HealthMonitor.h"
#include <cJSON.h>
// #include <ArduinoJson.h>

void OM2M_Post(String appliance_id, String user_status,float current, int helth, char motor_number);

char* ssid = "GALAXY KING";
char* passwd="DILEEPPRASANTHi";

long Channel_ID_1 = 2165368;
long Channel_ID_2 = 2165370;

String API_key1 = "899FMRYW1H2FPCNJ";
String API_key2 = "RLEHO8H1Z8C0I48Y";


String Client_ID = "CzYeCTwuJTkIHg0GITswBSo";
String mqttPass = "CzYeCTwuJTkIHg0GITswBSo";
String mqttUser = "dLNq6KNxZKZA6tU8dm3uDnTV";


//OM2M IMPLEMENTATION

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

WiFiClient client;
HTTPClient http;
PubSubClient mqttClient(client);

const char* server="http://smart-powergrid.000webhostapp.com/get_data.php";
const char* priorityserver="http://smart-powergrid.000webhostapp.com/priority.php";

// User user1(mqttUser, mqttPass,Channel_ID_1, API_key1);  
// User user2(mqttUser, mqttPass,Channel_ID_2, API_key2);  

#define led_ratedPower 0.09 
#define motor_ratedPower  1.7
#define buzzer_ratedPower 0.15  //NOTE: THESE VALUES ARE TAKEN FROM ONLINE SOURCES
#define power_source  5
#define led_res 90  //led resistence
#define motor_res 585   //motor resistence
#define buzzer_res  1500000 //buzzer resistence

#define user1_motors_common_pin 25
#define user1_motor1 26
#define user1_motor2 27 
#define user2_motors_common_pin 14
#define user2_motor1 12
#define user2_motor2 13

CurrentSensor u1m1(32);
CurrentSensor u1m2(33);
CurrentSensor u2m1(34);
CurrentSensor u2m2(35);

HealthMonitor u1m1health(0);
HealthMonitor u1m2health(0);
HealthMonitor u2m1health(0);
HealthMonitor u2m2health(0);

int User1motorpref;
int User2motorpref;

User user1("CzYeCTwuJTkIHg0GITswBSo","dLNq6KNxZKZA6tU8dm3uDnTV",Channel_ID_1,"899FMRYW1H2FPCNJ","EFISS04IFA6364N9");
User user2("CzYeCTwuJTkIHg0GITswBSo","dLNq6KNxZKZA6tU8dm3uDnTV",Channel_ID_2,"RLEHO8H1Z8C0I48Y","D3LNELVJ4YHFILVP");

//Resident_1: LED 1, LED 2, MOTOR 1, MOTOR 2
//Resident_2: LED 3, BUZZER, MOTOR 3, MOTOR 4
void setup() {
  pinMode(user1_motors_common_pin, INPUT);
  pinMode(user1_motor1, INPUT);
  pinMode(user1_motor2, INPUT);
  pinMode(user2_motors_common_pin, INPUT);
  pinMode(user2_motor1, INPUT);
  pinMode(user2_motor2, INPUT);

  WiFi.setHostname("MotorCurrentSensing");

  Serial.begin(115200);
  // Connect to Wi-Fi network
  WiFi.begin(ssid, passwd);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Wi-Fi connected, print the local IP address
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
 
  ThingSpeak.begin(client);      
  

}

#define maxCurrent_motor 100.0
#define minCurrent_motor 20.0


int voltages_raw[2][3];
double voltages[2];

// u1 motors direction: u1Status[4]
// u2 motors direction: u2Status[4]

double absf(double x){
  return x>0?x:-x;
}

String u1Status, u2Status;

const char* Error[2][2];
int helths[4];
// StaticJsonDocument<200> jsonDoc;

void loop() { 

  u1Status=ThingSpeak.readStringField(Channel_ID_1, 6, "EFISS04IFA6364N9"); //(channelid, field number, read apikey)
  u2Status=ThingSpeak.readStringField(Channel_ID_2, 7, "D3LNELVJ4YHFILVP"); //(channelid, field number, read apikey)
  Serial.println(ThingSpeak.getLastReadStatus());
  Serial.print("1) ");
  Serial.println(u1Status);
  Serial.print("2) ");
  Serial.println(u2Status);

  if(u1Status[2] == '0'){
    u1m1health.base_current = 48.0;
  }
  else if(u1Status[2] == '1'){
    u1m1health.base_current = 82.0;
  }
  else if(u1Status[2] == '2'){
    u1m2health.base_current = 100.0;
  }
  if(u1Status[8] == '0'){
    u1m2health.base_current = 48.0;
  }
  else if(u1Status[8] == '1'){
    u1m2health.base_current = 82.0;
  }
  else if(u1Status[8] == '2'){
    u1m2health.base_current = 100.0;
  }
  if(u2Status[8] == '0'){
    u2m1health.base_current = 48.0;
  }
  else if(u2Status[8] == '1'){
    u2m1health.base_current = 82.0;
  }
  else if(u2Status[8] == '2'){
    u2m1health.base_current = 100.0;
  }
  if(u2Status[8] == '0'){
    u2m2health.base_current = 48.0;
  }
  else if(u2Status[8] == '1'){
    u2m2health.base_current = 82.0;
  }
  else if(u2Status[8] == '2'){
    u2m2health.base_current = 100.0;
  }
  voltages_raw[0][0] = digitalRead(user1_motors_common_pin);
  voltages_raw[0][1] = digitalRead(user1_motor1);   // on if 1, off if 0
  voltages_raw[0][2] = digitalRead(user1_motor2);
  voltages_raw[1][0] = digitalRead(user2_motors_common_pin);
  voltages_raw[1][1] = digitalRead(user2_motor1);   // on if 0, off if 1
  voltages_raw[1][2] = digitalRead(user2_motor2);
  

  // voltages[0] = absf(voltages_raw[0][0] - voltages_raw[0][1]);
  // voltages[1] = absf(voltages_raw[1][0] - voltages_raw[1][1]);

  float currents[4] = {u1m1.getValueinmA(), u1m2.getValueinmA(), u2m1.getValueinmA(), u2m2.getValueinmA()};
  
  helths[0] = currents[0]!=0?u1m1health.calculate_health(currents[0]):helths[0];
  helths[1] = currents[1]!=0?u1m2health.calculate_health(currents[1]):helths[1];
  helths[2] = currents[2]!=0?u2m1health.calculate_health(currents[2]):helths[2];
  helths[3] = currents[3]!=0?u2m2health.calculate_health(currents[3]):helths[3];
  
  OM2M_Post(RES1_MOTOR_1, u1Status, currents[0], helths[0], 0);
  OM2M_Post(RES1_MOTOR_2, u1Status, currents[1], helths[1], 1);
  OM2M_Post(RES2_MOTOR_1, u2Status, currents[2], helths[2], 0);
  OM2M_Post(RES2_MOTOR_2, u2Status, currents[3], helths[3], 1);


  Serial.print("voltages: ");
  Serial.print(voltages_raw[0][0]);
  Serial.print(", ");
  Serial.print(voltages_raw[0][1]);
  Serial.print(", ");
  Serial.println(voltages_raw[0][2]);
  Serial.print(voltages_raw[1][0]);
  Serial.print(", ");
  Serial.print(voltages_raw[1][1]);
  Serial.print(", ");
  Serial.println(voltages_raw[1][2]);

  String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\"}";
  http.begin(priorityserver);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  if(httpResponseCode>0)
  {
    String payload = http.getString();
    // User1ledpref = int( payload[1]);
    User1motorpref = int(payload[0]-'0');
    

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
    // User1ledpref = int( payload[1]);
    User2motorpref = int(payload[0]-'0');
    

  }
  
    delay(500);
    
  if(u1Status[0]=='1' && voltages_raw[0][1] == voltages_raw[0][0]){
    Error[0][0] = "u1m1 line down";
    Serial.println("u1m1 line down");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Wire is down for Motor1!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);

  }
  if(u1Status[6]=='1' && voltages_raw[0][2] == voltages_raw[0][0]){
    Error[0][1] = "u1m2 line down";
    Serial.println("u1m2 line down");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Wire is down for Motor2!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  if(u1Status[0]=='0' && voltages_raw[0][1] != voltages_raw[0][0]){
    Error[0][0] = "u1m1 taking power when off";
    Serial.println("u1m1 taking power when off");
    
    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Motor1 is drawing power even though it is switched off (Power theft)!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);

  }
  if(u1Status[6]=='0' && voltages_raw[0][2] != voltages_raw[0][0]){
    Error[0][1] = "u1m2 taking power when off";
    Serial.println("u1m2 taking power when off");

    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Motor2 is drawing power even though it is switched off (Power theft)!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }

  if(u2Status[0]=='1' && voltages_raw[1][1] == voltages_raw[1][0]){
    Error[0][0] = "u2m1 line down";
    Serial.println("u2m1 line down");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Wire is down for Motor1!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);

  }
  if(u2Status[6]=='1' && voltages_raw[1][2] == voltages_raw[1][0]){
    Error[0][1] = "u2m2 line down";
    Serial.println("u2m2 line down");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Wire is down for Motor2!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }
  if(u2Status[0]=='0' && voltages_raw[1][1] != voltages_raw[1][0]){
    Error[0][0] = "u2m1 taking power when off";
    Serial.println("u2m1 taking power when off");
    
    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Motor1 is drawing power even though it is switched off (Power theft)!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);

  }
  if(u2Status[6]=='0' && voltages_raw[1][2] != voltages_raw[1][0]){
    Error[0][1] = "u2m2 taking power when off";
    Serial.println("u2m2 taking power when off");

    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Motor2 is drawing power even though it is switched off (Power theft)!\",\"appliance\":\"MOTORs\" }";
    // Serialize the JSON document to a string

    // Make an HTTP POST request
    http.begin(server);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonDoc);
    Serial.println(httpResponseCode);
    // Serial.print("Wire is down for Motor1");
    delay(500);
  }

if(User1motorpref==1){
  if(currents[0] > maxCurrent_motor || currents[1] > maxCurrent_motor){
    // float pot1_res = (power_source/maxCurrent_led) - Req_led;
    Serial.print("increase User1pot resistance");
    String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Increase potentiometer resistance\",\"appliance\":\"MOTORs\" }";

  // Serialize the JSON document to a string

  // Create an HTTP client object


  // Make an HTTP POST request
  http.begin(server);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  delay(500);
    // Serial.println(pot1_res);
  }
  if((u1Status[0]=='1' && currents[0] < minCurrent_motor )|| (u1Status[6]=='1' && currents[1] < minCurrent_motor)){
  Serial.print("lower the resistance of User1pot");
  String jsonDoc = "{\"user\":\"Resident1\", \"key\":\"1234\", \"msg\":\"Lower potentiometer resistance\",\"appliance\":\"MOTORs\" }";

  // Serialize the JSON document to a string

  // Create an HTTP client object


  // Make an HTTP POST request
  http.begin(server);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  delay(500);
  }
  }  

  // Serial.println(Error[0][0]);
  // Serial.println(Error[0][1]);
  // Serial.println(Error[1][0]);
  // Serial.println(Error[1][1]);
  // user1.mqttPublish(dataArray1, fieldArray1);
  // user2.mqttPublish(dataArray2, fieldArray2);
  delay(2000);



if(User2motorpref==1){
  if(currents[2] > maxCurrent_motor || currents[3] > maxCurrent_motor){
    // float pot1_res = (power_source/maxCurrent_led) - Req_led;
    Serial.print("increase User2pot resistance");
    String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Increase potentiometer resistance\",\"appliance\":\"MOTORs\" }";

  // Serialize the JSON document to a string

  // Create an HTTP client object


  // Make an HTTP POST request
  http.begin(server);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  delay(500);
    // Serial.println(pot1_res);
  }
  if((u2Status[0]=='1' && currents[2] < minCurrent_motor )|| (u2Status[6]=='1' && currents[3] < minCurrent_motor)){
  Serial.print("lower the resistance of User2pot");
  String jsonDoc = "{\"user\":\"Resident2\", \"key\":\"1234\", \"msg\":\"Lower potentiometer resistance\",\"appliance\":\"MOTORs\" }";

  // Serialize the JSON document to a string

  // Create an HTTP client object


  // Make an HTTP POST request
  http.begin(server);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc);
  Serial.println(httpResponseCode);
  delay(500);
  }
  }  

  // Serial.println(Error[0][0]);
  // Serial.println(Error[0][1]);
  // Serial.println(Error[1][0]);
  // Serial.println(Error[1][1]);
  // user1.mqttPublish(dataArray1, fieldArray1);
  // user2.mqttPublish(dataArray2, fieldArray2);
  delay(2000);
}

//RES1_MOTOR_1, u1Status, u1m1
void OM2M_Post(String appliance_id, String user_status,float current, int helth, char motor_number){
  String om2mserver ="http://" + String() + CSE_IP + ":" + String() + CSE_PORT + String()+ OM2M_MN + String() + OM2M_AE;
  http.begin(om2mserver + String() + appliance_id + "/");
  Serial.println(om2mserver + String() + appliance_id + "/");
  http.addHeader("X-M2M-Origin", OM2M_ORGIN);
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("Content-Length", "100");
  
  

  String send_data = String() + "{\"m2m:cin\": {"

  + "\"con\": \"" + user_status[0+6*motor_number] + "," + "20.10" + "," + String(current) + "," +user_status[2+6*motor_number] + "," + user_status[4+6*motor_number] 
  +  "," + String(helth) + "\","

  + "\"lbl\": \"data\""
  
  + "}}";
  Serial.println(send_data);
  int code = http.POST(send_data);
  http.end();
  Serial.println(code);
  delay(2000);
}


