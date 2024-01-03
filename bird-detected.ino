#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

const int pinBuzzer = 12;       // Pin buzzer dihubungkan ke pin 12 pada Arduino
const int pinMotor = 7;         // Pin motor DC dihubungkan ke pin 7 pada Arduino

bool birdDetected = false;

void setup() {
  Serial.begin(9600);           // Buka komunikasi serial dengan baud rate 9600
  pinMode(pinMotor, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);
  u8g2.begin();  // Initialize the OLED display
}

void loop() {
  digitalWrite(pinMotor, HIGH);
  OLED();
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n');
    if (received.equals("BIRD_DETECTED")) {
      birdDetected = true;
      secondloop();
      thirdloop();
      alarmOLED(); 
    } else {
      birdDetected = false;
      stopActions();
    }
  }
}

void secondloop() {
  digitalWrite(pinBuzzer, HIGH);
  delay(200);
  digitalWrite(pinBuzzer, LOW);
  delay(200);
  digitalWrite(pinBuzzer, HIGH);
  delay(200);
  digitalWrite(pinBuzzer, LOW);
  delay(1000);
}

void thirdloop() {
  digitalWrite(pinMotor, HIGH);
  delay(1000);
  digitalWrite(pinMotor, LOW);
  delay(1000);
}

void stopActions() {
  digitalWrite(pinMotor, LOW);
}

void OLED() {
  u8g2.clearBuffer();             
  u8g2.setBitmapMode(0); 
  u8g2.setFont(u8g2_font_inb16_mf); 
  u8g2.drawStr(0, 40, "YOLOIN"); 
  u8g2.sendBuffer();
}

void alarmOLED() {
  u8g2.clearBuffer();
  u8g2.setBitmapMode(0); 
  u8g2.setFont(u8g2_font_inb16_mf); 
  u8g2.drawStr(0, 40, "Bird !!!");
  u8g2.sendBuffer();
  delay(1000);
  u8g2.clearBuffer();              
  u8g2.setBitmapMode(0); 
  u8g2.setFont(u8g2_font_inb16_mf); 
  u8g2.drawStr(0, 40, "Bird !!!");
  delay(100);
}
