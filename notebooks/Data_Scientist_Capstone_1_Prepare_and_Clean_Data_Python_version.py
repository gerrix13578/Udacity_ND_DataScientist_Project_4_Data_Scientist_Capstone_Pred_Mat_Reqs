# %% [markdown]
# DATA SCIENTIST CAPSTONE PROJECT - PREPARE AND CLEAN DATA
# 
# Main goal of this part is to prepare the data to begin the analysis
# .
# As a input, there are two types of excel files: One with transactional data that is generated every day, and a second ond with master data.
# To analyse the data it is necessary to group all the columns in one data frame.
# 
# All the columns are not needed, so most of them will be ignored and I keep only the ones interesting for the analysis
# I only keep the rows that have values, because represent a process completed from the begining to the end. Rows with NaN values are eliminated.
# 
# Is necessary also to filter the rows that are in the scope. This means the ones that have a PLP value representative.
# 
# 

# %%
# Import libraries

import sys
import pandas as pd
import numpy as np
import glob
import sqlite3

# %% [markdown]
# Import the Data Files
# 
# Here we have two types
# - Transactional data with excel: Several files according to an initial and final date (4 first weeks October 2025)
# - Master date with excel: One file

# %%
# Import all the Excel Files that are in the data folder (Transactional data)

excel_files = glob.glob("data/*.xlsx")
df_transactional_all_data = pd.concat([pd.read_excel(f) for f in excel_files], ignore_index=True)

# Display the first rows
df_transactional_all_data.head()

# %%
# Import Excel file with Master data

# Path to the file
file_path = "master_data/Parasum_iTLS.xlsx"

# Read the Excel file
df_master_data = pd.read_excel(file_path)

# Display the first rows
print(df_master_data.head())


# %% [markdown]
# Merge Data
# 
# The 2 files have complementary columns that should be used in the analysis and prediction model. It is necessary to group them in one data frame

# %%
# Merge the 2 data frames using the Key colums: SFab, GLin, UbiLínea and Material. Both columns are in the 2 file types.
df_manual_requests = pd.merge(
    df_transactional_all_data,
    df_master_data,
    on=["SFab", "GLin", "UbiLínea", "Material"],
    how="left"  # or "inner" depending on your needs
)

df_manual_requests.head()

# %% [markdown]
# Filter Data 1 - Columns
# 
# Data frame for analysis is too big. It has a lot of columns that are no necessary.
# Note: All the column names are in Spanish.

# %%
# Subset the data frame with only the necessary columns for the analysis

# List of columns to keep
columns_to_keep = [
    "SFab","GLin","UbiLínea", "Material", "Denominación_x", "Status", "Tipo Sum", "Consumo",
    "F.Creac", "H.Creac", "F.Conf OT", "H.Conf OT", "Ubic.proc.",
    "Tp.alm.proc.", "UbicDest", "ÁrSumProd.", "Válido de", "Válido a", "Cap. Sumin"
]

# Subset the DataFrame
df_manual_requests = df_manual_requests[df_manual_requests.columns.intersection(columns_to_keep)]

df_manual_requests.head()

# %%
# Check the matrix size
df_manual_requests.shape

# %% [markdown]
# Clean Data: Drop Missing Values
# 
# Rows with NaN are useless, because represent incompleted processes.
# 

# %%
# Drop rows with any NaN values
df_manual_requests = df_manual_requests.dropna()

df_manual_requests.head()

# %%
# Check the matrix size
df_manual_requests.shape

# %% [markdown]
# Filter Data 2 - Rows
# 
# 
# Not all the data provided is usefull for the analysis.
# Scope:
# 
# Tipo Sum: NO and WN
# 
# SFab: 401, 402, 441 and 431
# 
# ÁrSumProd.: Should begin with "10", "09" or "08"

# %%

df_manual_requests_scope = df_manual_requests[
    (df_manual_requests["Tipo Sum"].isin(["NO", "WN"])) &
    (df_manual_requests["SFab"].isin([401, 402, 441, 431])) &
    (df_manual_requests["ÁrSumProd."].astype(str).str.startswith(("10", "09", "08")))
]

# Rename columns to better understand the analysis
df_manual_requests_scope = df_manual_requests_scope.rename(columns={
    'Denominación_x': 'Denominacion',
    'UbicDest': 'PLP',
    'ÁrSumProd.': 'PVB'
})

# Check the matrix size and first rows
print(df_manual_requests_scope.shape)
df_manual_requests_scope.head()

# %% [markdown]
# Add calculated Data
# 
# Now that all the basic data in the data frame is available, it is necessary to begin the calculations to add data needed for the analysis and the prediction model.
# 
# Supply Time: Duration in hours between the start of the event (Material Request) to the end of the event (Material Delivered)
# Time between MatReq: Duration in time between the first Material Request and the Second Material Request

# %%
# Make a copy to avoid SettingWithCopyWarning
df = df_manual_requests_scope.copy()

# Create two new col's in order to store the datetime in a format that can be used
# Specify the format (example: YYYY-MM-DD for date, HH:MM:SS for time)
df['datetime_creac'] = pd.to_datetime(df['F.Creac'] + ' ' + df['H.Creac'], format='%d.%m.%y %H:%M:%S', errors='coerce')
df['datetime_conf'] = pd.to_datetime(df['F.Conf OT'] + ' ' + df['H.Conf OT'], format='%d.%m.%y %H:%M', errors='coerce')


# Calculate Supply Time
df['Supply_time'] = df['datetime_conf'] - df['datetime_creac']

# Calculate Supply Time in hours
df['Supply_time_hours'] = df['Supply_time'].dt.total_seconds() / 3600

print(df[['datetime_creac', 'datetime_conf', 'Supply_time', 'Supply_time_hours']].head(10))

# Save stats_df to Excel for internal analysis
df.to_excel('SPA_Tiempos_entre_Peticion_y_Entrega_a_punto_consumo.xlsx', index=False)



# %%
# Calculate Time betwen Material Requests

# Sort by PLP and datetime_creac
df = df.sort_values(by=['PLP', 'datetime_creac'])

# Calculate time difference in hours between consecutive rows for each PLP
df['time_between_MatReqs'] = df.groupby('PLP')['datetime_creac'].diff().dt.total_seconds() / 3600


# Drop rows where 'time_between_reqs' is NaN
df = df.dropna(subset=['time_between_MatReqs'])

# Verify
print(df.shape)

print(df.head(20))


# %% [markdown]
# Store Data in a SQL DB
# 
# The Data is now prepared for the analysis process done in another Python script.
# 
# In this part, this data is stored in a local sql database in one single table.

# %%
# Define database name and table name
db_name = "SPA_Data_Analytics.db"  # SQLite databases are usually .db files
table_name = "SPA_Historic_Manual_Requests"


# Create a connection to the SQLite database
conn = sqlite3.connect(db_name)

# Store the DataFrame in the database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print(f"Data successfully stored in {db_name}, table: {table_name}")




