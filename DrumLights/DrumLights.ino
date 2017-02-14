#include "RunningAverage.h"

// These constants won't change.  They're used to give names
// to the pins used:
const int potPin = A7;  // Analog input pin that the potentiometer is attached to
const int piezoPin = A3;  // Analog input pin that the piezo is attached to
const unsigned long maxIn = 1023*1023; //Maximum range on multiplied input
const int analogOutPin = 13; // Analog output pin that the LED is attached to

unsigned int potValue = 0;        // value read from the pot
int piezoValue = 0;     // value from the piezo
RunningAverage smoothPiezo(30);; //Smooth out piezo values and crosstalk

int ledDelay = 0; //Light on time
int threshold = 0;
long prevMillis = 0; //previous turn on time for light delay

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(analogOutPin, OUTPUT);

  //Initialize smoothing
  smoothPiezo.addValue(0);
  smoothPiezo.addValue(0);
}

void loop() {
  // read the analog in value:
  potValue = analogRead(potPin); //This controls light delay
  piezoValue = analogRead(piezoPin); //This turns light on and off
  
  ledDelay = map(potValue,0,1024,0,500);
  threshold = map(potValue,0,1024,5,70);
  int diffPiezo = abs(piezoValue-smoothPiezo.getFastAverage());
  smoothPiezo.addValue(piezoValue);
  
  long currentMillis = millis();
  if(diffPiezo > threshold )
  {
    digitalWrite(analogOutPin, 1);
    prevMillis = millis();
  }
  if((currentMillis - prevMillis) > ledDelay)
  {
    digitalWrite(analogOutPin,0);
  }

  // print the results to the serial monitor:
  //Serial.println(diffPiezo);

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);
}

