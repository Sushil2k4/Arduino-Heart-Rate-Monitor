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

# Moving Average Filter
def moving_average(data, window_size=5):
    if len(data) < window_size:
        return data  # Return original data if not enough samples
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Function to calculate heart rate
def calculate_heart_rate(ppg_data):
    smoothed_ppg = moving_average(ppg_data)
    peaks = np.where(np.diff(np.sign(np.diff(smoothed_ppg))) < 0)[0] + 1
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
            try:
                ppg_value = int(ser.readline().decode().strip())  # Read PPG value from Arduino
                ppg_values.append(ppg_value)
            except ValueError:
                continue  # Ignore invalid data

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
