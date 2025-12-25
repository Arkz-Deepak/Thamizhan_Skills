#include <NewPing.h>


#define TRIG_PIN 9
#define ECHO_PIN 10
#define MOTOR_PIN 5 

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // 1. Send Pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // 2. Read Echo
  long duration = pulseIn(ECHO_PIN, HIGH);
  int distance = duration * 0.034 / 2;

  // 3. AI Logic (If-Else Rules)
  Serial.print("Distance: ");
  Serial.println(distance);

  if (distance < 20) {
    digitalWrite(MOTOR_PIN, LOW); // STOP
  } else {
    digitalWrite(MOTOR_PIN, HIGH); // GO
  }
  delay(100);
}