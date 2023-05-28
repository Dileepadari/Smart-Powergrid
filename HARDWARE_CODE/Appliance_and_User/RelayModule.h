class RelayModule {
  private:
  int pinNumber;
public:
  RelayModule() {
  }

  RelayModule(int pin) {
    pinNumber = pin;
    pinMode(pin, OUTPUT);
  }

  void commonToNO() {
    digitalWrite(pinNumber, LOW);
  }

  void commonToNC() {
    digitalWrite(pinNumber, HIGH);
  }
};