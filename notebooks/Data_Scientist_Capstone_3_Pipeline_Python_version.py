# %% [markdown]
# DATA SCIENTIST CAPSTONE - PIPELINE & PREDICTION VALUES
# 
# In this part we focus on how to predict the variable "Time between Requests" analysed before.
# As data to predict, we have these ones:
# - PLP id: Consumption Point identification
# - Material
# - Number of parts for each contanier in the Request - Assumed that each request needs only 1 container
# - Median of consumption parts per day in the Production process

# %%
# Import libraries

import pandas as pd
import numpy as np

import sqlite3


from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score


# %% [markdown]
# LOAD Data from Database
# 
# The database is based in sql lite. This database is generated in the Python script Data_Scientist_Capstone_1_Prepare_and_Clean_Data.jpynb

# %%
# Database and table details
db_name = "SPA_Data_Analytics.db"
table_name = "SPA_Historic_Manual_Requests"

# Connect to the SQLite database
conn = sqlite3.connect(db_name)

# Read the table into a DataFrame
df_loaded = pd.read_sql(f"SELECT * FROM {table_name}", conn)

# Close the connection
conn.close()

# Display the DataFrame
print(df_loaded.head())

# %% [markdown]
# Pipeline 1
# 
# First model to predict the variable "Time between Reqs" using the variables "Number of parts for each contanier in the Request", "Median of consumption parts per day in the Production process" and "Supply Time"

# %%
# Relevant columns
features = ['Consumo', 'Cap. Sumin', 'Supply_time_hours'] # These variables are "Median of consumption parts per day in the Production process", "Number of parts for each contanier in the Request" and "Supply Time"
target = 'time_between_MatReqs'

X = df_loaded[features]
y = df_loaded[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Scale features
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))  # Regression model
])

# Train the model
pipeline.fit(X_train, y_train)

# Predictions
y_pred = pipeline.predict(X_test)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RandomForest RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")


# %% [markdown]
# CONCLUSION Pipeline 1:
# 
# The Results indicate:
# 
# RMSE = 11.94 → The average prediction error is about 12 hours.
# R² = 0.38 → The model explains only 38% of the variance in Time between Requests
# 
# This suggests the model is underperforming, likely due to:
# - Feature relevance: X varibales may not strongly correlate with Y.
# - Data size: the dataset could be small for this type of prediction, so the model may not generalize well.
# - Hyperparameters: Default RandomForestRegressor settings may not be optimal.

# %% [markdown]
# Pipeline 2
# 
# In this case, I try to improve the model using RandomForest and GridSearchCV

# %%
# -------------------------------
# 1. RandomForest with GridSearch
# -------------------------------
rf_pipeline = Pipeline([
    ('scaler', StandardScaler()),  # optional for trees
    ('model', RandomForestRegressor(random_state=42))
])

rf_params = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [None, 10, 20],
    'model__min_samples_split': [2, 5]
}

rf_grid = GridSearchCV(rf_pipeline, rf_params, cv=3, scoring='r2', n_jobs=-1)
rf_grid.fit(X_train, y_train)

print("Best RF Params:", rf_grid.best_params_)

# Evaluate RF
rf_pred = rf_grid.predict(X_test)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2 = r2_score(y_test, rf_pred)

print(f"RandomForest -> RMSE: {rf_rmse:.2f}, R²: {rf_r2:.2f}")


# %% [markdown]
# CONCLUSION Pipeline 2:
# 
# Here we have an improvement with the RMSE and R² Parameters. So this model is better than the one done before to predict the "Time between Requests variable". 
# This means the tuned RandomForest is capturing more variance and making slightly more accurate predictions. However, the performance is still modest — R² of 0.44 suggests the model explains less than half of the variability.

# %% [markdown]
# Pipeline 3
# 
# Use of GradientBoosting for the model

# %%

# -------------------------------
# 2. GradientBoosting
# -------------------------------
gb_pipeline = Pipeline([
    ('scaler', StandardScaler()),  # optional for boosting
    ('model', GradientBoostingRegressor(random_state=42))
])

gb_pipeline.fit(X_train, y_train)
gb_pred = gb_pipeline.predict(X_test)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_r2 = r2_score(y_test, gb_pred)

print(f"GradientBoosting -> RMSE: {gb_rmse:.2f}, R²: {gb_r2:.2f}")


# %% [markdown]
# CONCLUSION Pipeline 3:
# 
# RandomForest still slightly outperforms GradientBoosting in this case

# %% [markdown]
# CONCLUSIONS:
# 
# Predict the Time between Requests it is not easier as it was expected: Depends hightly on the characteristics of each PLP (consumption point) as also seen in the analysis part of the project
# 
# NEXT STEPS:
# 
# Test with bigger amount of data (More than 4 weeks)
# Skip outliers on data: For example take in consideration that some requests are done just before weekend and the next one is after weekend when there is no production.
# Try to group the PLPs in groups with the same characteristics in order to build a better model
# 
# 


