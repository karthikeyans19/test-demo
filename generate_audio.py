import numpy as np
import base64

# Constants
SAMPLE_RATE = 4000  # Hz (samples per second)
DURATION = 5  # seconds

# Generate a sine wave as dummy audio data (for example, a 440 Hz tone)
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
frequency = 440  # Hz (A4 note)
audio_data = np.sin(2 * np.pi * frequency * t) * 32767  # Convert to range of int16
audio_data = audio_data.astype(np.int16)  # Convert to int16 format

# Encode the audio data to Base64 for transmission
encoded_audio = base64.b64encode(audio_data.tobytes()).decode('utf-8')

# Print the first 100 characters of the Base64 string for reference
print(encoded_audio[:100])  # Print the first 100 characters of the Base64 string