
# HearHere: Real-Time Speech-to-Text Transcription App

HearHere is a real-time speech-to-text transcription application that captures audio from the microphone, processes it using IBM Watson's Speech-to-Text API, and displays the transcriptions in a user-friendly graphical interface built with Tkinter. Ideal for creating accessible, live text captions, this app is perfect for those needing a continuous visual aid during spoken communication.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setting Up IBM Cloud & API Key](#setting-up-ibm-cloud--api-key)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Running the App](#running-the-app)
8. [How It Works](#how-it-works)
9. [Future Improvements](#future-improvements)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

**HearHere** transcribes live audio directly from your microphone and displays it in real-time within a Tkinter GUI, making it easy to follow spoken words visually. Leveraging IBM Watson’s powerful Large Speech Models (LSM), it’s built for accuracy and responsiveness, providing an accessible solution to those who need continuous transcription.

## Features

- **Real-time, continuous transcription** of microphone audio.
- **IBM Watson Large Speech Models (LSM)** for improved recognition accuracy.
- **Responsive, easy-to-use GUI** with Tkinter.
- **Auto-reconnection** if WebSocket or API connection is interrupted.

---

## Requirements

Ensure the following prerequisites are met before proceeding:

- **Python** 3.8 or higher
- **pip** package manager

### Python Packages

The required Python packages are listed in the `requirements.txt` file in the repository.

---

## Setting Up IBM Cloud & API Key

1. **Create an IBM Cloud Account**  
   - Go to [IBM Cloud](https://cloud.ibm.com/) and sign up or log in.
   - Navigate to the dashboard after logging in.

2. **Create a Speech-to-Text Service**  
   - In the dashboard, select **Create Resource**.
   - Search for "Speech to Text" and select it.
   - Choose the **Lite** or **Standard** plan based on your usage needs.
   - Pick the region nearest to you for optimal performance (e.g., `us-south`).

3. **Enable Large Speech Model (LSM)**  
   - Go to the **Manage** tab of your Speech-to-Text service.
   - Select **English (United States) - en-US** to use the Large Speech Model for greater accuracy.

4. **Obtain API Key & URL**  
   - Under **Credentials** in the **Manage** tab, locate your **API Key** and **URL**.  
   - These credentials will be required for configuring the app.

---

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/LukeZem/HearHere.git
    cd HearHere
    ```

2. **Install Dependencies**

    Install all required packages listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    **Note**: If `pyaudio` encounters installation errors, it may require platform-specific installation steps. See [PyAudio Installation Documentation](https://pypi.org/project/PyAudio/).

---

## Configuration

1. **Environment Variables**  
   - Create a `.env` file in the project’s root directory and add the following lines:

    ```plaintext
    API_KEY=your_ibm_api_key
    URL=your_ibm_service_url
    ```

2. **Set Up Region**  
   Ensure the `URL` matches the selected IBM Cloud region, for example:
   ```plaintext
   wss://api.us-south.speech-to-text.watson.cloud.ibm.com/v1/recognize
   ```

---

## Running the App

Start the application by running:

```bash
python your_app_name.py
```

The GUI window will open, capturing audio from your microphone and displaying transcriptions in real-time.

---

## How It Works

1. **Audio Capture**  
   - Captures live audio input from the microphone using `pyaudio`.
   
2. **WebSocket Connection**  
   - Establishes a connection to IBM Watson via WebSocket for continuous, low-latency communication.

3. **Speech Recognition**  
   - Utilizes IBM Watson’s LSM for high-quality speech recognition.

4. **Real-Time Display**  
   - Transcriptions appear in real-time on a Tkinter GUI.

5. **Error Handling**  
   - Reconnects automatically if there’s an interruption in the WebSocket connection.

---

## Future Improvements

The following features are planned for future releases of HearHere to improve functionality and usability:

- **Automatic Line Breaks Based on Pause Detection**  
    Detects natural pauses in speech and inserts line breaks for improved readability.

- **Grammar and Syntax Prediction**  
    Integrates Natural Language Processing (NLP) for more accurate sentence structuring.

- **Export Options for Dialogs**  
    Enables saving transcriptions to various formats, such as DOCX, PDF, and TXT, for archival or sharing purposes.

- **Customizable Transcription Settings**  
    Allows users to adjust settings, such as font size, color scheme, and text alignment, directly in the GUI.

---

## Troubleshooting

1. **WebSocket Errors**  
   - Ensure that the `.env` file contains the correct API Key and URL.
   
2. **PyAudio Installation Issues**  
   - Some systems require specific steps for `pyaudio`. Check [PyAudio’s Documentation](https://pypi.org/project/PyAudio/) for guidance.

---

## Contributing

Contributions are welcome! Feel free to open issues, discuss improvements, or submit pull requests.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
