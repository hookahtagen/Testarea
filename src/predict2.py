import sqlite3
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from datetime import datetime, timezone, timedelta
from sklearn.linear_model import LinearRegression

# Connect to database
conn = sqlite3.connect('../data/weather.db')
c = conn.cursor()

# Get data from the last 5 minutes
now = datetime.now(timezone.utc)
five_minutes_ago = now - timedelta(minutes=5)
query = f"SELECT timestamp, temperature, pressure, humidity FROM environment_data WHERE timestamp >= {five_minutes_ago.timestamp()}"

# Get data from the database
data = c.execute(query).fetchall()

# Create input and output arrays for polynomial regression
X = []
y = []
for i in range(len(data)-1):
    temp, pressure, humidity = data[i][1], data[i][2], data[i][3]
    next_temp = data[i+1][1]
    X.append([temp, pressure, humidity])
    y.append(next_temp)

# Create polynomial regression pipeline
degree = 2  # degree of polynomial regression
model = make_pipeline(PolynomialFeatures(degree), LinearRegression())

# Fit the model on the input and output arrays
model.fit(X, y)

# Predict the temperature 10 minutes into the future
last_temp, last_pressure, last_humidity = data[-1][1], data[-1][2], data[-1][3]
future_pressure, future_humidity = last_pressure, last_humidity
future_time = datetime.fromtimestamp(data[-1][0] + 600)

# Create input array for future prediction
future_X = np.array([[last_temp, future_pressure, future_humidity]])

# Use the trained model to predict the temperature
future_temp = model.predict(future_X)[0]

# Print the prediction
print(f"The temperature at {future_time} is predicted to be {future_temp:.1f} degrees Celsius.")