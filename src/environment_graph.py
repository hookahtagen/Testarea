import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

# Connect to the weather database
conn = sqlite3.connect('../data/weather.db')
c = conn.cursor()

# Retrieve the data from the environment_data table
c.execute("SELECT timestamp, temperature, pressure, humidity FROM environment_data")
data = c.fetchall()

# Extract the values into separate lists
timestamps = [row[0] for row in data]
temperatures = [row[1] for row in data]
pressures = [row[2] for row in data]
humidities = [row[3] for row in data]

# Create the graph
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
fig.suptitle('Weather Data')

ax1.plot(timestamps, temperatures, color='red')
ax1.set_ylabel('Temperature (°C)')
ax1.set_ylim([-20, 40])

ax2.plot(timestamps, pressures, color='blue')
ax2.set_ylabel('Pressure (hPa)')
ax2.set_ylim([800, 1300])

ax3.plot(timestamps, humidities, color='green')
ax3.set_ylabel('Humidity (%)')
ax3.set_ylim([0, 100])

form= '%Y-%m-%d'
# Set x-axis ticks to show dates every 10 days
start_date = time.strftime(form, time.localtime(timestamps[0]))
end_date = time.strftime(form, time.localtime(timestamps[-1]))
ax3.xaxis.set_major_locator(mdates.DayLocator(interval=10))
ax3.xaxis.set_major_formatter(mdates.DateFormatter(form))
ax3.set_xlim([start_date, end_date])

plt.show()
