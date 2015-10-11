/* 
This provides a serial interface for the MSGEQ7 IC. It first sends a 255,
then the value of each channel ranging from 0 to 254. Running on an Attiny85.

Original code and hardware build notes:
http://www.instructables.com/id/How-to-build-your-own-LED-Color-Organ-Arduino-MSGE/?ALLSTEPS
*/

#include <SoftwareSerial.h>

SoftwareSerial serial (0, 1);
const int analogPin = 3;
const int strobePin = 4;
const int resetPin = 2;
int spectrumValue[7];
const int filter = 80;

void setup() {	
	serial.begin(9600);
	pinMode(analogPin, INPUT);
	pinMode(strobePin, OUTPUT);
	pinMode(resetPin, OUTPUT);
	digitalWrite(resetPin, LOW);
	digitalWrite(strobePin, HIGH);
}

void loop() {
	serial.write(255);
	digitalWrite(resetPin, HIGH);
	digitalWrite(resetPin, LOW);
	for (int i = 0; i < 7; i++) {
		digitalWrite(strobePin, LOW);
		delay(1);
		spectrumValue[i] = analogRead(analogPin);
		spectrumValue[i] = constrain(spectrumValue[i], filter, 1023);
		spectrumValue[i] = map(spectrumValue[i], filter, 1023, 0, 254);
		serial.write(spectrumValue[i]);
		digitalWrite(strobePin, HIGH);
	}
}