const int ppgSensorPin = A0;  // PPG sensor connected to analog pin A0
const int sampleSize = 10;    // Number of samples for smoothing
const int threshold = 600;    // Threshold for peak detection (adjust based on sensor output)
const int interval = 5000;    // Time interval for BPM calculation (5 seconds)

int ppgValues[sampleSize];    // Array to store sensor readings
int peakCount = 0;            // Count detected peaks
unsigned long startTime;      // Start time for BPM calculation

void setup() {
  Serial.begin(9600);         // Initialize serial communication
  startTime = millis();       // Record the start time
}

void loop() {
  int smoothedValue = getSmoothedReading();  // Get smoothed PPG value

  // Detect peaks based on threshold
  static int lastValue = 0;
  if (smoothedValue > threshold && lastValue <= threshold) {
    peakCount++;
  }
  lastValue = smoothedValue;

  // Calculate BPM every 'interval' milliseconds
  if (millis() - startTime >= interval) {
    int bpm = (peakCount * 60000) / interval;  // Convert peaks to BPM
    Serial.print("Heart Rate: ");
    Serial.print(bpm);
    Serial.println(" BPM");

    // Reset counters
    peakCount = 0;
    startTime = millis();
  }

  delay(50);  // Small delay for better sampling
}

// Function to get a smoothed PPG reading
int getSmoothedReading() {
  int sum = 0;
  for (int i = 0; i < sampleSize; i++) {
    ppgValues[i] = analogRead(ppgSensorPin);
    sum += ppgValues[i];
    delay(2);  // Small delay for stability
  }
  return sum / sampleSize;
}
