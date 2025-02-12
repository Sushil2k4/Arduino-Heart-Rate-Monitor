import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# Serial communication setup
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's port
time.sleep(2)  # Allow time for serial connection to establish

# Variables for heart rate calculation
ppg_values = []
time_window = 10  # Time window in seconds for heart rate calculation
sampling_rate = 10  # Samples per second

# Function to calculate heart rate
def calculate_heart_rate(ppg_data):
    peaks = np.where(np.diff(np.sign(np.diff(ppg_data))) < 0)[0] + 1
    if len(peaks) > 1:
        heart_rate = len(peaks) / (time_window / 60)  # Beats per minute
        return heart_rate
    return 0

# Real-time heart rate monitoring
try:
    print("Starting heart rate monitoring...")
    start_time = time.time()
    while True:
        if ser.in_waiting > 0:
            ppg_value = int(ser.readline().decode().strip())  # Read PPG value from Arduino
            ppg_values.append(ppg_value)

            # Process data in time windows
            if time.time() - start_time >= time_window:
                heart_rate = calculate_heart_rate(ppg_values)
                print(f"Heart Rate: {heart_rate:.2f} BPM")
                ppg_values = []  # Reset PPG values for the next window
                start_time = time.time()

except KeyboardInterrupt:
    print("Heart rate monitoring stopped.")
finally:
    ser.close()  # Close serial connection