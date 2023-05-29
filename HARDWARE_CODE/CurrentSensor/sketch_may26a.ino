#include "CurrentSensor.h"
CurrentSensor csensor(14);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(14,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(csensor.getValueinA());
  delay(2000);
}
