#include <HX711.h>
#include <CapacitiveSensor.h>

CapacitiveSensor cs1 = CapacitiveSensor(2, 3); // 1MOhm resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
CapacitiveSensor cs2 = CapacitiveSensor(4, 5); // 1MOhm resistor between pins 4 & 6, pin 6 is sensor pin, add a wire and or foil

// HX711(Data pin, Clock pin)
HX711 scale1(A0, A1), scale2(A2, A3);

// sensor activation threshold
#define THRESHOLD 250

// sensor states
bool state1, state2;

long last_send = 0;

void setup() {
  Serial.begin(115200);

  // disable calibration
  cs1.set_CS_AutocaL_Millis(0xFFFFFFFF);
  cs2.set_CS_AutocaL_Millis(0xFFFFFFFF);

  // test calibration
  scale1.set_scale(1952.3392857142858);
  scale1.tare();

  scale2.set_scale(-1968.857142857143);
  scale2.tare();


  last_send = millis();
}

// 00000000
// _______0 : message typte = input
// ______s_ : button 1 state
// _____s__ : button 2 state
void send_input_msg() {
  byte c = (state2 ? (1 << 2) : 0) | (state1 ? (1 << 1) : 0);
  Serial.write(c);
  // Serial.println(c, DEC);
}

void loop() {

  long total1 =  cs1.capacitiveSensor(15);
  long total2 =  cs2.capacitiveSensor(15);

  if(total1 > THRESHOLD) {
    if(!state1) {
      state1 = true;
      send_input_msg();
    }
  } else {
    if(state1) {
      state1 = false;
      send_input_msg();
    }
  }

  if(total2 > THRESHOLD) {
    if(!state2) {
      state2 = true;
      send_input_msg();
    }
  } else {
    if(state2) {
      state2 = false;
      send_input_msg();
    }
  }

  if(millis() - last_send > 1000) {
    unsigned int w1 = constrain(scale1.get_units(1), 0, 5000);
    unsigned int w2 = constrain(scale2.get_units(1), 0, 5000);

    Serial.write(1);
    Serial.write((byte*)&w1, 2);
    Serial.write((byte*)&w2, 2);

    last_send = millis();
  }
}
