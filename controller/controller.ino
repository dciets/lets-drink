#include <CapacitiveSensor.h>

CapacitiveSensor cs1 = CapacitiveSensor(2, 3); // 1MOhm resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
CapacitiveSensor cs2 = CapacitiveSensor(5, 6); // 1MOhm resistor between pins 4 & 6, pin 6 is sensor pin, add a wire and or foil

// sensor activation threshold
#define THRESHOLD 250

// sensor states
bool state1, state2;
bool weight1, weight2;

long last_send = 0;

void setup() {
  Serial.begin(115200);

  // disable calibration
  cs1.set_CS_AutocaL_Millis(0xFFFFFFFF);
  cs2.set_CS_AutocaL_Millis(0xFFFFFFFF);

  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
}

// 00000000
// _______0 : message typte = input
// ______s_ : button 1 state
// _____s__ : button 2 state
// ____w___ : weight 1 state
// ___w____ : weight 2 state
void send_input_msg() {
  byte c = (state2 << 2) | (state1 << 1) | (weight1 << 3) | (weight2 << 4);
  Serial.write(c);
  // Serial.println(c, DEC);
}

void loop() {
  bool changed = false;
  
  long total1 = cs1.capacitiveSensor(15);
  long total2 = cs2.capacitiveSensor(15);
  
  bool w1 = digitalRead(8);
  bool w2 = digitalRead(9);

  if(total1 > THRESHOLD) {
    if(!state1) {
      state1 = true;
      changed = true;
    }
  } else {
    if(state1) {
      state1 = false;digitalWrite(A0, weight1);
      changed = true;
    }
  }

  if(total2 > THRESHOLD) {
    if(!state2) {
      state2 = true;
      changed = true;
    }
  } else {
    if(state2) {
      state2 = false;
      changed = true;
    }
  }

  if(w1 != weight1) {
    weight1 = w1;
    changed = true;
  }

  if(w2 != weight2) {
    weight2 = w2;
    changed = true;
  }

  if(changed) {
    send_input_msg();
  }
  
  digitalWrite(A0, !w1);
  digitalWrite(A2, w1);
  digitalWrite(A5, !w2);
  digitalWrite(A4, w2);

  delay(15);
}
