#include "CurrentSensor.h"
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


String Client_ID = "CzYeCTwuJTkIHg0GITswBSo";
String mqttPass = "CzYeCTwuJTkIHg0GITswBSo";
String mqttUser = "dLNq6KNxZKZA6tU8dm3uDnTV";

WiFiClient client;
PubSubClient mqttClient(client);

User user1(mqttUser, mqttPass,Channel_ID_1, API_key1);  
User user2(mqttUser, mqttPass,Channel_ID_2, API_key2);  

#define led_ratedPower 0.09 
#define motor_ratedPower  1.7
#define buzzer_ratedPower 0.15  //NOTE: THESE VALUES ARE TAKEN FROM ONLINE SOURCES
#define power_source  5
#define led_res 90  //led resistence
#define motor_res 585   //motor resistence
#define buzzer_res  1500000 //buzzer resistence


// CurrentSensor csensor1(18);
// CurrentSensor csensor2(19);
// CurrentSensor csensor3(20);
// CurrentSensor csensor4(21);
// CurrentSensor csensor5(22);
// CurrentSensor csensor6(23);
// CurrentSensor csensor7(24);
// CurrentSensor csensor8(25);

CurrentSensor current_sensors[] = {CurrentSensor(18), CurrentSensor(19), CurrentSensor(20), CurrentSensor(21), CurrentSensor(22), CurrentSensor(23), CurrentSensor(24), CurrentSensor(25)};

//defining maximum current that can pass through each component - led/buzzer/motor; with a 0.9 factor for safety purposes
float maxCurrent_led = (led_ratedPower/power_source)*0.9;
float maxCurrent_motor = (motor_ratedPower/power_source)*0.9;
float maxCurrent_buzzer = (buzzer_ratedPower/power_source)*0.9;


//finding the equivalent resistances
float Req_led = (led_res)/3;  //LED group's equivalent resistance
float Req_motor = (motor_res)/4;  //DC Motor group's equivalent
float Req_buzzer = buzzer_res;  //Buzzer resistence

//Resident_1: LED 1, LED 2, MOTOR 1, MOTOR 2
//Resident_2: LED 3, BUZZER, MOTOR 3, MOTOR 4
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(18,INPUT);  //LED 1
  pinMode(19,INPUT);  //LED 2
  pinMode(20,INPUT);  //LED 3
  pinMode(21,INPUT);  //BUZZER
  pinMode(22,INPUT);  //MOTOR 1
  pinMode(23,INPUT);  //MOTOR 2
  pinMode(24,INPUT);  //MOTOR 3
  pinMode(25,INPUT);  //MOTOR 4
}

void loop() {
  // put your main code here, to run repeatedly:
  float current_readings[8];
  for(int i = 0; i<8; i++){
    current_readings[i] = current_sensors[i].getValueinA();
    float current[] = {current_readings[i]};  
    if(i == 0){//LED 1 current
      int fieldarray[] = {0,0,0,1,0,0,0,0};
      user1.mqttPublish(current, fieldarray);      
    }
    if(i == 1){//LED 2 current
      int fieldarray[] = {0,0,0,0,1,0,0,0};
      user1.mqttPublish(current, fieldarray); 
    }
    if(i == 2){//LED 3 current
      int fieldarray[] = {0,0,1,0,0,0,0,0};
      user2.mqttPublish(current, fieldarray); 
    }
    if(i == 3){//BUZZER current
      int fieldarray[] = {0,0,0,0,1,0,0,0};
      user2.mqttPublish(current, fieldarray); 
    }
    if(i == 4){//MOTOR 1 current
      int fieldarray[] = {1,0,0,0,0,0,0,0};
      user1.mqttPublish(current, fieldarray); 
    }
    if(i == 5){//MOTOR 2 current
      int fieldarray[] = {0,0,1,0,0,0,0,0};
      user1.mqttPublish(current, fieldarray); 
    }
    if(i == 6){//MOTOR 3 current
      int fieldarray[] = {1,0,0,0,0,0,0,0};
      user2.mqttPublish(current, fieldarray);   
    }
    if(i == 7){//MOTOR 4 current
      int fieldarray[] = {0,1,0,0,0,0,0,0};
      user2.mqttPublish(current, fieldarray); 
    }
  }


  // float i1 = csensor1.getValueinA();//led 1
  // float i2 = csensor2.getValueinA();//led 2
  // float i3 = csensor3.getValueinA();//buzzer
  // float i4 = csensor4.getValueinA();//motor 1
  // float i5 = csensor5.getValueinA();//motor 2
  // float i6 = csensor6.getValueinA();//motor 3
  // float i7 = csensor7.getValueinA();//motor 4
  // float i8 = csensor8.getValueinA();//motor 5
  // Serial.println(i1);
  // Serial.println(i2);
  // Serial.println(i3);
  // Serial.println(i4);
  // Serial.println(i5);
  // Serial.println(i6);
  // Serial.println(i7);
  // Serial.println(i8);


  //if either of the current sensors [for LEDs] exceed the threshold; calculate the resistance to which potentiometer must be updated and put an alert
  if(current_readings[0] > maxCurrent_led || current_readings[1] > maxCurrent_led || current_readind[2] ){
    float pot1_res = (power_source/maxCurrent_led) - Req_led;
    Serial.print("Set LED - potentiometer to ");
    Serial.println(pot1_res);
  }
  //if current sensor [for buzzer] exceed the threshold; calculate the resistance to which potentiometer must be updated and put an alert  
  if(current_readings[3] > maxCurrent_buzzer){
    float pot2_res = (power_source/maxCurrent_buzzer)-Req_buzzer;
    Serial.print("Set Buzzer - potentiometer to ");
    Serial.println(pot2_res);    
  }
  //if either of the current sensors [for motors] exceed the threshold; calculate the resistance to which potentiometer must be updated and put an alert
  if(current_readings[4] > maxCurrent_motor || current_readings[5] > maxCurrent_motor || current_readings[6] > maxCurrent_motor || current_readings[7] > maxCurrent_motor){
    float pot3_res = (power_source/maxCurrent_motor) - Req_motor;
    Serial.print("Set Motor - potentiometer to ");
    Serial.println(pot3_res);
  }  

  delay(2000);
}
