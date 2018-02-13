#include <CapacitiveSensor.h>

CapacitiveSensor cs1 = CapacitiveSensor(2, 3); // 1MOhm resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
CapacitiveSensor cs2 = CapacitiveSensor(4, 5); // 1MOhm resistor between pins 4 & 6, pin 6 is sensor pin, add a wire and or foil

// sensor activation threshold
#define THRESHOLD 300

// sensor states
bool state1, state2;

void setup() {
  Serial.begin(115200);

  // disable calibration
  cs1.set_CS_AutocaL_Millis(0xFFFFFFFF);
  cs2.set_CS_AutocaL_Millis(0xFFFFFFFF);
}

// 00000000
// _______0 : message typte = input
// ______s_ : button 1 state
// _____s__ : button 2 state
void send_input_msg() {
  byte c = (state2 ? (1 << 2) : 0) | (state1 ? (1 << 1) : 0);
  Serial.write(c);
}

void loop() {
  long total1 =  cs1.capacitiveSensor(15);
  long total2 =  cs2.capacitiveSensor(15);

  // Serial.println(total1 > 250 ? 21 );

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

  delay(15);
}
