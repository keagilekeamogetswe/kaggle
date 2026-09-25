from load_data import CSV_DIR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
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

print("Print 5 houses prediction.", melbourne_model.predict(X.head()))


predicted_home_prices = melbourne_model.predict(X)
print("Mean Absolute Error:", mean_absolute_error(y, predicted_home_prices))