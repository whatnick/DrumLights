// RunningAverage class 
// based on RunningAverage library for Arduino
// source:  http://playground.arduino.cc/Main/RunningAverage
#include "RunningAverage.h"

// These constants won't change.  They're used to give names
// to the pins used:
const int potPin = A0;  // Analog input pin that the potentiometer is attached to
const int piezoPin = A1;  // Analog input pin that the piezo is attached to
const unsigned long maxIn = 1023*1023; //Maximum range on multiplied input
const int green_out = 3; // Analog output pin that the LED is attached to
const int red_out = 5; // Analog output pin that the LED is attached to
const int blue_out = 6; // Analog output pin that the LED is attached to

int red_val,green_val,blue_val;

unsigned int potValue = 0;        // value read from the pot
int piezoValue = 0;     // value from the piezo
RunningAverage smoothPiezo(30);; //Smooth out piezo values and crosstalk

int ledDelay = 0; //Light on time
int noise_thresh = 400;
long prevMillis = 0; //previous turn on time for light delay

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(green_out, OUTPUT);
  pinMode(red_out, OUTPUT);
  pinMode(blue_out, OUTPUT);

  //Initialize smoothing
  smoothPiezo.addValue(0);
  smoothPiezo.addValue(0);
}

void loop() {
  // read the analog in value:
  potValue = analogRead(potPin); //This controls light delay
  piezoValue = analogRead(piezoPin); //This turns light on and off
  
  ledDelay = map(potValue,0,1024,0,500);

  int diffPiezo = abs(piezoValue-smoothPiezo.getFastAverage());
  smoothPiezo.addValue(piezoValue);
  
  long currentMillis = millis();
  long beat_time = 0;
  if(diffPiezo > noise_thresh )
  {
    beat_time = currentMillis-prevMillis;
    if(beat_time > 25)
    {
      blue_val = map(beat_time,100,300,0,255);
      if(beat_time > 300) blue_val = 0;
      green_val = map(beat_time,200,500,0,255);
      if(beat_time > 600) green_val = 0;
      red_val = map(beat_time,400,800,0,255);
      if(beat_time > 1000) 
      {
        blue_val = 255;
        green_val = 255;
      }
      analogWrite(blue_out, blue_val);
      analogWrite(green_out, green_val);
      analogWrite(red_out, red_val);
      Serial.println(beat_time);
      prevMillis = millis();
    }
  }
  if((currentMillis - prevMillis) > ledDelay)
  {
    red_val = green_val = blue_val = 0;
    analogWrite(blue_out, blue_val);
    analogWrite(green_out, green_val);
    analogWrite(red_out, red_val);
  }



  // print the results to the serial monitor:
  if(beat_time>50)
  {
    
  }

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);
}
