class Motor{
  String UserID;
  int EnablePin1;
  int EnablePin2;
  int InputPin1;
  int InputPin2;
  int PWMChannel;
  
public:

  Motor(String userID, int enablePin1, int enablePin2, int inputPin1, int inputPin2, int pwmChannel){
    UserID = userID;
    EnablePin1 = enablePin1;
    EnablePin2 = enablePin2;
    InputPin1 = inputPin1;
    InputPin2 = inputPin2;
    PWMChannel = pwmChannel;
  }

  void Setup(){
    pinMode(EnablePin1, OUTPUT);
    pinMode(EnablePin2, OUTPUT);
    pinMode(InputPin1, OUTPUT);
    pinMode(InputPin2, OUTPUT);
    ledcSetup(PWMChannel, 30000, 8); // default values initially
    ledcAttachPin(EnablePin1, PWMChannel);
    ledcAttachPin(EnablePin2, PWMChannel);
    Serial.println("setup done");
  }

  void SwitchOn(){
    // set to default direction forward
    digitalWrite(InputPin1, LOW);
    digitalWrite(InputPin2, HIGH);
  }
  
  void TurnOn(){
    digitalWrite(EnablePin1, HIGH);
    digitalWrite(EnablePin2, HIGH);
    Serial.println("turned on");
  }

  void SwitchOff(){
    digitalWrite(InputPin1, LOW);
    digitalWrite(InputPin2, LOW);
    Serial.println("switched off");    
  }

  void Kill(){
    digitalWrite(EnablePin1, LOW);
    digitalWrite(EnablePin2, LOW);
    Serial.println("killed"); 
  }

  void SetSpeed(int SpeedLevel){
    // 0: low, 1: medium, 2: high (full speed)
    if(SpeedLevel==0){
      ledcWrite(PWMChannel, 40);
    }
    else if(SpeedLevel == 1){
      ledcWrite(PWMChannel, 120);
    }
    else if(SpeedLevel == 2){
      ledcWrite(PWMChannel, 255);
    }
    Serial.print("Speed: ");
    Serial.println(SpeedLevel);
  }

  void SetDirection(int Direction){
    // assuming 1 for forward, 0 for backward
    // default forward
    if(Direction==1){
      digitalWrite(InputPin1, LOW);
      digitalWrite(InputPin2, HIGH);
    }
    else if(Direction==0){
      digitalWrite(InputPin1, HIGH);
      digitalWrite(InputPin2, LOW);
    }
    Serial.print("Direction: ");
    Serial.println(Direction);
  }
};