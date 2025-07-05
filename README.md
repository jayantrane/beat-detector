# Raspberry Pi Audio Lighting

This project turns your Raspberry Pi into a real-time audio visualizer. It analyzes a music file and controls the brightness of an LED based on the music's intensity, creating a simple but effective light show. The script can play audio from a local file or a URL.

## Features

-   **Real-time Audio Analysis**: Analyzes music to extract its energy/intensity.
-   **Dynamic LED Brightness**: Uses Pulse-Width Modulation (PWM) to make an LED's brightness correspond to the music's volume.
-   **Simultaneous Playback**: Plays the music while visualizing it.
-   **Flexible Input**: Works with local audio files (`.mp3`, `.wav`, etc.) or audio from a URL.

## Hardware Requirements

-   A Raspberry Pi (any model with GPIO pins)
-   An LED
-   A 330 Ohm resistor (or similar)
-   Jumper wires
-   Speakers or headphones connected to the Raspberry Pi

## Hardware Setup

1.  Connect the longer leg (anode) of the LED to GPIO pin 17 on the Raspberry Pi.
2.  Connect the shorter leg (cathode) of the LED to one end of the 330 Ohm resistor.
3.  Connect the other end of the resistor to a Ground pin (GND) on the Raspberry Pi.

```
   Raspberry Pi
      │
 (GPIO 17)
      │
     (+)
     LED
     (-)
      │
   Resistor (330Ω)
      │
    (GND)
      │
```

## Software Setup

This project uses Python 3.

1.  **Clone or Download:**
    Get the project files onto your Raspberry Pi.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install the necessary Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

The script can be run from the terminal. You can specify a path to a local audio file or a URL. If you don't provide a source, it will look for a file named `song.mp3` in the same directory.

**Default (using `song.mp3`):**
```bash
python beat_detector.py
```

**With a local audio file:**
```bash
python beat_detector.py /path/to/your/music.mp3
```

**With a URL:**
The script will download the audio before playing.
```bash
python beat_detector.py https://example.com/path/to/your/music.mp3
```

## Creative Enhancements

This project can be expanded in many creative ways:

-   **Beat-Synchronized Flashing**: Modify the code to detect sharp beats (`librosa.beat.beat_track`) and make the LED flash in sync with the rhythm.
-   **RGB Color Visualization**: Use an RGB LED (`gpiozero.RGBLED`) and map different frequencies (bass, mids, treble) to different colors for a more vibrant light show.
-   **Multiple LEDs**: Expand the setup to control multiple LEDs, creating more complex patterns and light displays.
