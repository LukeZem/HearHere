"""
Author: Lucas Zemlin
Date: 10/25/2024
Overview: This application provides real-time speech-to-text transcription. It 
captures audio from the microphone, sends it to the IBM Watson service, and displays 
the transcriptions in a Tkinter GUI.

Dependencies:
- json: Handles JSON data. Used to parse and generate JSON strings. Essential for 
    communication with APIs that use JSON format.
- threading: Manages concurrent threads. Creates and runs multiple threads. Allows 
    simultaneous execution of tasks, improving performance.
- time: Provides time-related functions. Used for delays and timestamps. Necessary 
    for timing operations and pauses in execution.
- tkinter: Creates the graphical user interface (GUI). Provides widgets like windows, 
    buttons, and text boxes. Enables user interaction with the program through a GUI.
- websocket: Facilitates WebSocket communication. Connects to IBM Watson's WebSocket 
    API. Required for real-time, bidirectional communication with the service.
- base64: Encodes and decodes Base64 data. Encodes the API key for authentication. 
    Ensures secure transmission of credentials.
- pyaudio: Captures audio from the microphone. Interfaces with the system's audio 
    input. Needed to capture live audio for processing and transcription.
- numpy: Performs numerical operations. Provides functions for array manipulation 
    and math operations. Useful for processing audio data, though not directly used 
    in this script.
- os: Accesses environment variables. Retrieves values from the system environment. 
    Allows configuration through environment variables.
- dotenv: Loads environment variables from a .env file. Reads key-value pairs from 
    the file and sets them as environment variables. Simplifies configuration 
    management by storing settings in a file.

Technologies:
- IBM Watson Speech-to-Text: A cloud-based service for converting speech into text.
- Tkinter: A standard Python library for creating graphical user interfaces.
- WebSocket: A protocol for full-duplex communication channels over a single TCP 
    connection.
- PyAudio: A library for working with audio streams.
"""

import json
import threading
import time
import tkinter as tk
from websocket import create_connection, WebSocketConnectionClosedException
import base64
import pyaudio
import numpy as np
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve IBM Watson Speech-to-Text credentials
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set in the environment variables.")
url = os.getenv("URL")
if not url:
    raise ValueError("URL is not set in the environment variables.")

# IBM Watson Speech-to-Text credentials
auth_string = f"apikey:{api_key}"
auth_base64 = base64.b64encode(auth_string.encode()).decode()


# GUI setup
root = tk.Tk()
root.title("Real-Time Text to Speech Display (ALPHA)")
root.geometry("700x600")
root.configure(bg="#2E2E2E")

title_label = tk.Label(
    root,
    text="Real-Time Text to Speech for Grandma :)",
    font=("Arial", 16, "italic"),
    fg="#FFFFFF",
    bg="#2E2E2E",
    pady=10,
)
title_label.pack()

# Text box for transcriptions
text_box = tk.Text(
    root,
    font=("Helvetica", 20),
    wrap="word",
    fg="#FFFFFF",
    bg="#1E1E1E",
    insertbackground="white",
    padx=10,
    pady=10,
    state="disabled",
    borderwidth=0,
)
text_box.pack(expand=True, fill="both", padx=20, pady=(10, 20))

# Audio settings with adjusted chunk size
chunk_size = 512  # Slightly increased chunk size for stability
audio_format = pyaudio.paInt16
channels = 1
rate = 16000

audio = pyaudio.PyAudio()
stream = audio.open(
    format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size
)

# Track the last update time for pause detection
last_update_time = time.time()
silence_threshold = 5  # Number of seconds before line break

def connect_and_transcribe():
    """
    Establishes a WebSocket connection to the IBM Watson Speech-to-Text service 
    and initiates the transcription process. The function attempts to connect to 
    the WebSocket API, sending initialization parameters upon connection.
    
    Returns:
        WebSocket: The WebSocket connection object for ongoing communication.
    
    Raises:
        Exception: If the connection attempt fails, the function retries after 
        a short delay.
    """
    headers = [f"Authorization: Basic {auth_base64}"]

    while True:
        try:
            ws = create_connection(url, header=headers)
            init_message = json.dumps(
                {
                    "action": "start",
                    "content-type": "audio/l16; rate=16000; channels=1",
                    "interim_results": True,  # Enables partial results for faster updates
                    "timestamps": False,
                    "inactivity_timeout": -1,
                }
            )
            ws.send(init_message)
            print("Connected to IBM Watson Speech-to-Text. Listening...")

            threading.Thread(target=receive_transcription, args=(ws,), daemon=True).start()
            return ws

        except Exception as e:
            print(f"Failed to connect: {e}. Retrying in 2 seconds...")
            time.sleep(2)


def receive_transcription(ws):
    """
    Receives and processes transcription results from the WebSocket connection.
    
    Args:
        ws (WebSocket): The WebSocket connection object to IBM Watson.
    
    Functionality:
        Continuously listens for transcription responses, differentiates 
        between final and interim results, and updates the GUI text box in real 
        time. Final results replace interim text for improved readability.
    
    Handles:
        WebSocket disconnections gracefully, reattempting connections as needed.
    """
    global last_update_time
    last_partial = ""  # Track the last partial transcript
    last_final = ""  # Track the last final transcript

    try:
        while True:
            result = ws.recv()
            result_dict = json.loads(result)

            if "results" in result_dict:
                transcript = result_dict["results"][0]["alternatives"][0]["transcript"]
                is_final = result_dict["results"][0]["final"]
                current_time = time.time()

                text_box.config(state="normal")

                if is_final:
                    # Clear partial text and add final result as persistent text
                    if transcript != last_final:
                        text_box.delete("end-1c linestart", "end")
                        text_box.insert("end", transcript + " ")
                        last_final = transcript  # Update last final transcript
                        last_partial = ""  # Clear the partial text
                        last_update_time = current_time
                        print("Final: ", transcript)  # Log final result
                else:
                    # Display partial immediately and replace previous partial
                    if transcript != last_partial:
                        text_box.delete("end-1c linestart", "end")
                        text_box.insert("end", transcript)
                        last_partial = transcript
                        print("Partial: ", transcript)  # Log partial for debugging

                # Autoscroll to the bottom
                text_box.config(state="disabled")
                text_box.see("end")

    except WebSocketConnectionClosedException:
        print("WebSocket connection closed. Reconnecting...")
        connect_and_transcribe()
    except Exception as e:
        print(f"Unexpected WebSocket error: {e}. Attempting reconnection...")
        time.sleep(2)
        connect_and_transcribe()


def listen_and_stream(ws):
    """
    Captures live audio from the microphone and streams it to the IBM Watson 
    Speech-to-Text service via WebSocket.
    
    Args:
        ws (WebSocket): The WebSocket connection to which audio data is sent.
    
    Mechanism:
        Audio is read in real time from the microphone, converted to the required 
        format, and transmitted over the WebSocket. Error handling is included 
        to address connection interruptions.
    """
    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            ws.send(data, opcode=0x2)
    except Exception as e:
        print(f"Audio streaming error: {e}")
        restart_stream(ws)


def restart_stream(ws):
    """
    Restarts the audio stream if an error occurs, maintaining continuous audio 
    capture and streaming.
    
    Args:
        ws (WebSocket): The WebSocket connection to IBM Watson.
    
    Purpose:
        Provides robustness by reinitializing the audio stream and resuming 
        the audio transmission, minimizing downtime during transcription.
    """
    global stream
    stream.stop_stream()
    stream.close()
    time.sleep(1)  # Brief delay to ensure resources are released
    stream = audio.open(
        format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size
    )
    listen_and_stream(ws)  # Resume streaming


def on_closing():
    """
    Handles the graceful shutdown of the application, ensuring all resources 
    are released.
    
    Actions:
        Stops and closes the audio stream, terminates the PyAudio instance, and 
        closes the GUI window.
    """
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Audio stream closed.")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Start threads
ws = connect_and_transcribe()
threading.Thread(target=listen_and_stream, args=(ws,), daemon=True).start()

root.mainloop()
