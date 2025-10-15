import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Dummy dataset
data = pd.DataFrame({
    'impressions': [1000, 2000, 3000, 4000, 5000],
    'clicks': [100, 150, 300, 350, 400],
    'conversions': [10, 20, 35, 40, 50]
})

X = data[['impressions', 'clicks']]
y = data['conversions']

model = RandomForestRegressor()
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Model trained and saved as model.pkl')
