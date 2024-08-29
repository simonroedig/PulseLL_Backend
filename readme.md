# PulseLL Backend

## Overview

PulseLL is a IOS Application designed to enhance the workout experience through real-time, AI-generated music that adapts to the user's physiological data. This repository houses all the backend code necessary to process workout data, communicate with ChatGPT, and generate dynamic, responsive music for users via generating code for Sonic Pi.

## Frontend Repository

This repository only contains the backend code for PulseLL. The corresponding frontend code, which handles the user interface and data collection from wearable devices, can be found in the [PulseLL Frontend Repository](https://github.com/tudi2d/piis_pulsell).

## Why PulseLL?

Physical exercise is often more enjoyable and effective when accompanied by music, especially when the music is tailored to the specific activity and pace of the workout. Research has shown that music can positively influence both psychological and physiological aspects of exercise, enhancing the duration and quality of the workout experience. However, manually managing music during a workout can be disruptive and counterproductive. PulseLL addresses this by creating an intelligent system that automatically generates and adjusts music based on real-time workout data, eliminating the need for manual interaction.

## What Does PulseLL (Backend) Do?

The backend processes physiological data sent from a wearable device (such as an Apple Watch), decides when the workout's intensity requires a change in music, and then generates a new track using ChatGPT to generate code that is executed in Sonic Pi. The system ensures that the music evolves with the workout, maintaining a seamless flow and enhancing the overall exercise experience.

Key functionalities include:

- **Real-time Data Processing:** Continuously receives and processes heart rate and workout data from the frontend.
- **Dynamic Music Generation:** Uses OpenAI’s ChatGPT to generate Sonic Pi code for music that matches the user's workout intensity and preferences.
- **Seamless Music Transition:** Smoothly transitions between tracks based on changes in the user's physiological state.
- **Live Audio Streaming:** Streams the generated music in real-time back to the user.

## How is PulseLL Implemented?

The backend architecture of PulseLL is implemented using a Python server built with the Flask framework. The architecture features several critical components:

1. **Vital Threshold Logic:** Monitors heart rate changes to determine when new music should be generated.
2. **Prompt Constructor:** Builds prompts for ChatGPT based on the current workout data, which generates the corresponding Sonic Pi code.
3. **Sonic Pi Integration:** Executes the Sonic Pi code, generating music that is played in real-time.
4. **Audio Streaming:** Utilizes PyAudio (with VB-Audio’s Virtual Cable to capture system sound) and FFMPEG to stream the generated music live to the frontend.

## Repository Structure

This repository contains all the backend code for PulseLL. The code is organized into modules that manage data processing, ChatGPT interactions, music generation, and streaming. 

- `main.py`: The main Flask application file, where routes and logic are defined.
- `vital_threshold_logic.py`: Contains the logic for determining when to change the music based on heart rate data.
- `prompt_constructor.py`: Handles the creation of prompts for ChatGPT.
- `sonic_pi.py and run_stop_sonic_pi.py`: Manages communication with Sonic Pi and the execution of generated code.
- `audio_streaming.py`: Implements the live audio streaming functionality.
