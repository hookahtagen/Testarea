import os
import pyaudio
import struct
import numpy as np

# Konfiguration
CHUNKSIZE = 1024 # Anzahl der Samples pro Chunk
FORMAT = pyaudio.paInt16 # Format der Audiosamples
CHANNELS = 1 # Anzahl der Audio-Kanäle
RATE = 44100 # Samplerate
THRESHOLD = 2000 # Schwellenwert für Klick-Erkennung

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT, 
    channels=CHANNELS, 
    rate=RATE,
    input=True, 
    frames_per_buffer=CHUNKSIZE)

def clear_screen():
    os.system('clear')

def count_clicks(data):
    data = np.array(struct.unpack("%dh" % (len(data)/2), data))
    peak = np.max(np.abs(data))
    if peak > THRESHOLD:
        return 1
    else:
        return 0

count = 0
clear_screen()

while True:
    try:
        data = stream.read(CHUNKSIZE, exception_on_overflow=False)
        clicks = count_clicks(data)
        count += clicks
        print("Klicks: {}".format(count), end='\r')
    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()
p.terminate()
