from load_data import CSV_DIR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import pandas as pd

# Load data
melbourne_data = pd.read_csv(CSV_DIR)

# Filter rows with missing price values
filtered_melbourne_data = melbourne_data.dropna(axis=0)
# Choose target and features
y = filtered_melbourne_data.Price
features = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt', 'Lattitude', 'Longtitude']
X = filtered_melbourne_data[features]

# Define model
melbourne_model = DecisionTreeRegressor()
# Fit model
melbourne_model.fit(X, y)

predicted_home_prices = melbourne_model.predict(X)
print("Mean Absolute Error using trained data:", mean_absolute_error(y, predicted_home_prices))

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
melbourne_model.fit(train_X, train_y)

# get predicted prices on validation data
val_predictions = melbourne_model.predict(val_X)
print("Mean Absolute Error from an untrained dataset:", mean_absolute_error(val_y, val_predictions))