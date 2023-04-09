import pyaudio
import numpy as np
import time

# Schwellenwert für die Klick-Erkennung
threshold = 0.01

# Anzahl der Samples, die pro Sekunde aufgenommen werden
sample_rate = 44100

# Dauer einer Messung in Sekunden
measurement_duration = 60

# Initialisiere PyAudio
p = pyaudio.PyAudio()

# Öffne den Mikrofon-Eingang
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=1024)

print("Starte Messung...")

# Zähle die Klicks seit Programmstart
click_count_total = 0

# Endlosschleife
while True:
    # Zähle die Klicks während der aktuellen Messung
    click_count = 0
    
    # Array zur Speicherung der Samples während einer Messung
    samples = np.zeros(int(measurement_duration * sample_rate))

    # Startzeitpunkt der Messung
    start_time = time.time()

    # Aufnahme starten
    for i in range(len(samples)):
        # Lese ein Sample aus dem Stream
        sample = np.frombuffer(stream.read(1024), dtype=np.float32)[0]

        # Speichere das Sample im Array
        samples[i] = sample

        # Wenn das Sample den Schwellenwert überschreitet, erhöhe den Klick-Counter
        if sample > threshold:
            click_count += 1
            click_count_total += 1

    # Aufnahme beenden
    stream.stop_stream()
    stream.close()

    # Berechne die Anzahl der Klicks pro Minute (CPM)
    cpm = click_count / measurement_duration * 60

    # Gib die Ergebnisse aus
    print("Klicks pro Minute: {:.2f}".format(cpm))
    print("Gesamtzahl der Klicks: {}".format(click_count_total))

    # Öffne den Mikrofon-Eingang für die nächste Messung
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)

