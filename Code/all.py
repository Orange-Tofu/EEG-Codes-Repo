import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import threading
import time

import warnings

# Suppress the Matplotlib warning
warnings.filterwarnings("ignore", category=UserWarning)

filename = r'M:\CS\MainPro\EEG\Dataset\Alphawaves\subject_00.mat'


def eyesStatus():
    mat_data = sio.loadmat(filename) # Replace with your file path

    # Access EEG data from the loaded .mat file
    eeg_data = mat_data['SIGNAL'] # Replace 'SIGNAL' with the actual variable name

    # Define the electrode names and their corresponding channel indices
    electrode_info = {
    'FP1': 0,
    'FP2': 1,
    'FC5': 2,
    'FC6': 3,
    'FZ': 4,
    'T7': 5,
    'CZ': 6,
    'T8': 7,
    'P7': 8,
    'P3': 9,
    'PZ': 10,
    'P4': 11,
    'P8': 12,
    'O1': 13,
    'Oz': 14,
    'O2': 15
    }

    # Define the time vector for plotting (assuming a specific sample rate)
    sample_rate = 512 # Sample rate in Hz, modify as needed
    timer = np.arange(0, len(eeg_data)) / sample_rate

    # Extract data from FP1 and FP2 electrodes
    fp1_data = eeg_data[:, electrode_info['FP1']]
    fp2_data = eeg_data[:, electrode_info['FP2']]

    # Calculate the difference between FP1 and FP2 data
    difference_data = fp2_data - fp1_data

    # Define window size for moving average (modify as needed)
    window_size = 512 # Samples, modify as needed

    # Apply moving average to difference data
    smoothed_data = np.convolve(difference_data, np.ones(window_size) / window_size, mode='same')

    # Define threshold for detecting eye closure (modify as needed)
    threshold = 2300 # Microvolts, modify as needed

    # Initialize state variable to track eye state
    eye_state = "open"

    # Function to process the signal in real-time
    def process_signal():
        nonlocal threshold, eye_state
        
        start_time = time.time()
        i = 0
        
        while i < len(smoothed_data):
            if (timer[i] == 55.0):
                threshold = 2150
            
            if smoothed_data[i] < threshold and eye_state == "open":
                print(f"Time: {timer[i]:.2f} seconds - eyes closed")
                eye_state = "closed"
            elif smoothed_data[i] >= threshold and eye_state == "closed":
                print(f"Time: {timer[i]:.2f} seconds - eyes open")
                eye_state = "open"
            
            elapsed_time = time.time() - start_time
            
            if elapsed_time < timer[i]:
                time.sleep(timer[i] - elapsed_time)
            
            i += 1

    # Create a thread for processing the signal in real-time
    signal_thread = threading.Thread(target=process_signal)

    # Start the thread
    signal_thread.start()

    # Wait for the thread to finish (optional)
    signal_thread.join()
    print("The END")


def stopwatch():
    # input("Press Enter to start the stopwatch.")
    start_time = time.time()
    duration = 123
    try:
        while True:
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Elapsed time: {int(hours)}h {int(minutes)}m {int(seconds)}s", end="\r")
            if elapsed_time >= duration:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopwatch stopped.")
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Total elapsed time: {int(hours)}h {int(minutes)}m {int(seconds)}s")



def graphical():
    mat_data = sio.loadmat(filename)  # Replace with your file path

    # Access EEG data from the loaded .mat file
    eeg_data = mat_data['SIGNAL']  # Replace 'SIGNAL' with the actual variable name

    # Define the electrode names and their corresponding channel indices
    electrode_info = {
        'FP1': 0,
        'FP2': 1,
        'FC5': 2,
        'FC6': 3,
        'FZ': 4,
        'T7': 5,
        'CZ': 6,
        'T8': 7,
        'P7': 8,
        'P3': 9,
        'PZ': 10,
        'P4': 11,
        'P8': 12,
        'O1': 13,
        'Oz': 14,
        'O2': 15
    }

    # Define the time vector for processing (assuming a specific sample rate)
    sample_rate = 512  # Sample rate in Hz, modify as needed
    timer = np.arange(0, len(eeg_data)) / sample_rate

    # Extract data from FP1 and FP2 electrodes
    fp1_data = eeg_data[:, electrode_info['FP1']]
    fp2_data = eeg_data[:, electrode_info['FP2']]

    # Calculate the difference between FP1 and FP2 data
    difference_data = fp2_data - fp1_data

    # Define the scrolling window size (in seconds)
    window_size = 10000  # Modify as needed

    # Create a figure and axis for the scrolling plot
    fig, ax = plt.subplots(figsize=(12, 4))
    line, = ax.plot([], [], label='FP2 - FP1', color='b')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('EEG Data Difference (uV)')
    ax.set_title('Real-Time EEG Data Difference (Strip Chart Recorder)')
    ax.legend()
    ax.grid(True)

    # Initialize variables for the scrolling plot
    num_points_to_display = int(window_size * sample_rate)
    x_data = []
    y_data = []

    # Function to update the scrolling plot with new data
    def update_plot(i):
        nonlocal x_data, y_data

        # Append the new data point to the arrays
        x_data.append(timer[i])
        y_data.append(difference_data[i])

        # Truncate arrays to the specified window size
        if len(x_data) > num_points_to_display:
            x_data = x_data[-num_points_to_display:]
            y_data = y_data[-num_points_to_display:]

        # Update the plot data
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

    # Animate the scrolling plot with a faster update rate
    update_rate = 33  # Increase this value to update the plot more quickly
    start_time = time.time()
    for i in range(0, len(timer), update_rate):
        update_plot(i)
        
        # Calculate the elapsed time since the start
        elapsed_time = time.time() - start_time
        
        # Calculate the time interval for the next update
        time_interval = 1 / update_rate
        
        # Adjust the pause duration based on elapsed time
        pause_duration = max(0, time_interval - elapsed_time)
        time.sleep(pause_duration)
        plt.pause(0.001)  # Pause to allow the plot to update

    # Disable interactive mode after the loop
    plt.ioff()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Create threads for each function
    thread1 = threading.Thread(target=stopwatch)
    thread2 = threading.Thread(target=graphical)
    thread3 = threading.Thread(target=eyesStatus)

    # Start all three threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish (optional)
    thread1.join()
    thread2.join()
    thread3.join()