#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"
#include "Ultrasonic.h"
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

Ultrasonic ultrasonic(7);

TinyGPSPlus gps;
SoftwareSerial SoftSerial(6, 7);


const int mpuAddress = 0x68;  
MPU6050 mpu(mpuAddress);

int ax, ay, az;
int gx, gy, gz;

long tiempo_prev;

float dt;
float ang_x, ang_y;
float ang_x_prev, ang_y_prev;

long old_ultrasonic = 0;

void updateFiltered() {
   dt = (millis() - tiempo_prev) / 1000.0;
   tiempo_prev = millis();

   float accel_ang_x = atan(ay / sqrt(pow(ax, 2) + pow(az, 2)))*(180.0 / 3.14);
   float accel_ang_y = atan(-ax / sqrt(pow(ay, 2) + pow(az, 2)))*(180.0 / 3.14);

   ang_x = 0.98*(ang_x_prev + (gx / 131)*dt) + 0.02*accel_ang_x;
   ang_y = 0.98*(ang_y_prev + (gy / 131)*dt) + 0.02*accel_ang_y;
   ang_x_prev = ang_x;
   ang_y_prev = ang_y;
}

void displayGPSInfo() {
  if (gps.location.isValid()) {
    Serial.print("Location: ");
    Serial.print(gps.location.lat(), 6);
    Serial.print(", ");
    Serial.println(gps.location.lng(), 6);
  } else {
    Serial.println("Location: 0, 0");
  }
}

void setup() {
   Serial.begin(115200);
   SoftSerial.begin(9600);
   Wire.begin(9600);
   mpu.initialize();
}

void loop() {

    if(SoftSerial.available()) {
      while (SoftSerial.available()) {
        if (gps.encode(SoftSerial.read())) {
          displayGPSInfo();
          delay(100);
          break;
        }  
      } 
    } 

    long RangeInCentimeters = ultrasonic.MeasureInCentimeters();
    
    if (RangeInCentimeters < 500 && RangeInCentimeters > 0) {
      if (old_ultrasonic != RangeInCentimeters) {
        old_ultrasonic = RangeInCentimeters;
        Serial.print("Ultrasonic: ");
        Serial.println(RangeInCentimeters, DEC);  
        delay(100);
      }
    }

    mpu.getAcceleration(&ax, &ay, &az);
    mpu.getRotation(&gx, &gy, &gz);
    updateFiltered();
    
    if (45 < ang_x || ang_x < -45) {
      Serial.print("Pitch: ");
      Serial.println(ang_x);
      delay(100);
    }
    if (45 < ang_y || ang_y < -45) {
      Serial.print("Roll: ");
      Serial.println(ang_y);
      delay(100);
    }
}