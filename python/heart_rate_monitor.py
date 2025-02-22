import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import csv

# Serial communication setup
ser = serial.Serial('COM3', 9600, timeout=1)  # Added timeout for better handling
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

# Function to calculate heart rate using adaptive peak detection
def calculate_heart_rate(ppg_data):
    if len(ppg_data) < sampling_rate * time_window:
        return 0  # Not enough data points to calculate heart rate
    smoothed_ppg = moving_average(ppg_data)
    peaks, _ = find_peaks(smoothed_ppg, distance=sampling_rate/2, height=np.mean(smoothed_ppg))
    if len(peaks) > 1:
        heart_rate = (len(peaks) / time_window) * 60  # Beats per minute
        return heart_rate
    return 0

# Function to log data to a CSV file
def log_data(ppg_values, heart_rate):
    with open("heart_rate_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), heart_rate, *ppg_values])

# Real-time heart rate monitoring with plotting
try:
    print("Starting heart rate monitoring...")
    start_time = time.time()
    plt.ion()  # Enable interactive mode for real-time plotting
    fig, ax = plt.subplots()
    
    # Create CSV file with headers
    with open("heart_rate_data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Heart Rate (BPM)", "PPG Values"])
    
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
                log_data(ppg_values, heart_rate)  # Log data to CSV
                
                # Update real-time plot
                ax.clear()
                ax.plot(ppg_values, label='PPG Signal')
                ax.set_title("PPG Signal Over Time")
                ax.set_xlabel("Samples")
                ax.set_ylabel("PPG Value")
                ax.legend()
                plt.draw()
                plt.pause(0.01)
                
                ppg_values = []  # Reset PPG values for the next window
                start_time = time.time()

except KeyboardInterrupt:
    print("Heart rate monitoring stopped.")
finally:
    ser.close()  # Close serial connection
    plt.ioff()
    plt.show()  # Show final plot
