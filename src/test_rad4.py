import os
import sqlite3
import struct
from threading import Thread
import pyaudio
import numpy as np
import time


class constants:
    CHUNKSIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    THRESHOLD = 7500

    DATA_DELAY = 60


class RadDetector:
    def __init__(self, name: str) -> None:
        self.name = name
        self.CHUNKSIZE = constants.CHUNKSIZE
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = constants.CHANNELS
        self.RATE = constants.RATE
        self.THRESHOLD = constants.THRESHOLD

        self.detector_thread = Thread(target=self.detector, daemon=True)
        self.is_running = False

        self.count = 0
        self.count_since_start = 0

        self.database = constants.database
        self.conn = None
        self.conn = self.db_connect()

    def db_connect(self) -> sqlite3.connect:
        self.conn = None

        try:
            con = sqlite3.connect(self.database)
            print("Connection to database established.")
        except sqlite3.Error as e:
            print(f"Error encountered while connecting to the database: {e}")
            con = -1

        return con
    
   # def update_data_point(self, con: sqlite3.connect, data: tuple) -> bool:
        ack = False
        
        # data values
        time_stamp = time.time()
        start_time = self.start_time
        total_clicks = self.count_since_start
        counts_per_minute = self.cpm
        time_stamp, temperature, pressure, humidity = data
        
        values = (time_stamp, temperature, pressure, humidity)
        
        sql_query = "INSERT INTO environment_data (timestamp, temperature, pressure, humidity) VALUES (?, ?, ?, ?)"

        try:
            # Insert the data into the database
            cursor = con.cursor()
            cursor.execute(sql_query, values)
            con.commit()
            ack = True
        except sqlite3.Error as e:
            print(f"Error encountered while saving data to the database: {e}")
            ack = False
        finally:
            if ack is False:
                con.rollback()
            elif ack is True:
                print("Data point saved to database.")

        return ack

    def detector(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNKSIZE)

        while self.is_running:
            data = stream.read(self.CHUNKSIZE, exception_on_overflow=False)
            clicks = self.count_clicks(data)
            self.count += clicks
            self.count_since_start = self.count            

        print("Measurement stopped by user.")
        stream.stop_stream()
        stream.close()
        p.terminate()

    def start(self):
        self.is_running = True
        self.detector_thread.start()

    def stop(self):
        self.is_running = False

    def count_clicks(self, data):
        data = np.array(struct.unpack("%dh" % (len(data)/2), data))
        peak = np.max(np.abs(data))
        if peak > self.THRESHOLD:
            return 1
        else:
            return 0


def clear_screen():
    os.system('clear')


def print_data(cpm: float, count_since_start: int):

    i = 0
    for _ in range(constants.DATA_DELAY):
        clear_screen()
        print(f"Klicks seit Start:\t{count_since_start}")
        print(f"Klicks pro Minute:\t{cpm}")
        print(f"\nNächste Daten in {constants.DATA_DELAY - i} Sekunden")

        i += 1
        time.sleep(1)


def setup():
    pass


if __name__ == '__main__':

    rad_detector = RadDetector("gm-tube")
    rad_detector.start()

    start_time = time.time()

    time.sleep(1)
    clear_screen()

    try:

        for i in range(constants.DATA_DELAY):
            print("Starting....")
            print(f"Data available in {constants.DATA_DELAY - i} seconds")
            time.sleep(1)
            clear_screen()

        while True:
            elapsed_time = time.time() - start_time
            cpm = rad_detector.count / elapsed_time * constants.DATA_DELAY
            print_data(cpm, rad_detector.count_since_start)

    except KeyboardInterrupt:
        rad_detector.stop()
