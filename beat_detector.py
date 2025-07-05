
import librosa
import numpy as np
import pygame
import time
from gpiozero import LED
import argparse
import requests
import os

# GPIO pin for the LED
LED_PIN = 17

def play_music(file_path):
    """
    Initializes pygame and plays the music file.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def detect_high_modulation(file_path, threshold=0.1):
    """
    Analyzes a music file to control an LED based on music intensity.
    It checks the intensity every 200 milliseconds.

    Args:
        file_path (str): The path to the music file.
        threshold (float): The energy threshold for detecting high modulation.
    """
    led = LED(LED_PIN)
    led_state = False # Keep track of the current LED state

    try:
        # 1. Load the audio file
        y, sr = librosa.load(file_path)

        # 2. Set the frame size to 200ms
        hop_duration = 0.2  # seconds
        hop_length = int(hop_duration * sr)

        # 3. Calculate the root-mean-square (RMS) energy for each frame
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]

        # 4. Normalize the RMS energy to a range of 0-1
        if np.max(rms) > 0:
            rms = rms / np.max(rms)

        # 5. Play the music
        play_music(file_path)

        # 6. Control the LED based on the music intensity
        for energy in rms:
            new_state = energy > threshold
            if new_state != led_state:
                if new_state:
                    led.on()
                    print("High")
                else:
                    led.off()
                led_state = new_state
            
            time.sleep(hop_duration) # Wait for the duration of the frame

    except Exception as e:
        print(f"Error processing file: {e}")
    finally:
        led.off() # Ensure the LED is off when the script finishes
        pygame.mixer.music.stop()

def download_file(url, local_filename):
    """Downloads a file from a URL."""
    print(f"Downloading from {url}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music visualizer with LED control.")
    parser.add_argument("music_source", nargs='?', default="song.mp3",
                        help="Path or URL to the music file. Defaults to song.mp3")
    args = parser.parse_args()

    music_file = args.music_source

    # Check if the source is a URL
    if music_file.startswith('http://') or music_file.startswith('https://'):
        music_file = download_file(music_file, "downloaded_song.mp3")
        if not music_file:
            exit() # Exit if download fails
    elif not os.path.exists(music_file):
        print(f"Error: File not found at {music_file}")
        exit()

    print(f"Analyzing {music_file}...")
    detect_high_modulation(music_file)
