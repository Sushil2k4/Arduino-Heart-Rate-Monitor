// Arduino Code for Heart Rate Sensor
const int ppgSensorPin = A0;  // PPG sensor connected to analog pin A0

void setup() {
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  int ppgValue = analogRead(ppgSensorPin);  // Read PPG sensor value
  Serial.println(ppgValue);                 // Send PPG value to serial monitor
  delay(100);                               // Delay for stability
}