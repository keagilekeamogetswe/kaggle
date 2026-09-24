from load_data import CSV_DIR
from sklearn.tree import DecisionTreeRegressor
import pandas as pd

df = pd.read_csv(CSV_DIR)
# Choosing feature
features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']
price = df.Price
pruned_data_frame = df[features]
all_cols = df.columns
print(pruned_data_frame.head())
print("All cols: ", all_cols)
print(pruned_data_frame.describe())

# Define model. Specify a number for random_state to ensure same results each run
model = DecisionTreeRegressor(random_state = 1)
model.fit(pruned_data_frame, price)

#print("Making predictions for the following 5 houses:")

print(model.predict(pruned_data_frame.head()))