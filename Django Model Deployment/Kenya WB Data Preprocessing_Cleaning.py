import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel('Kenya World Bank Data (2013-2022).xlsx')
df = df.transpose() # Transpose the dataframe ie rows to columns and columns to rows
df.columns = df.iloc[0] # Set the first row as the column names
df = df[1:] # Remove the first row                                  
df = df.dropna(axis=0, how='all') # Remove all NaN values
df = df.drop(df.index[0]) # drop the first row at index 0
df = df.dropna(axis=0, how='all')
df = df.drop(df.columns[0], axis=1) # drop the first column at index 0

df = df.rename(columns={'Series Name': 'Year'}) # Rename columns
df = df.replace('..', 0.0)
df = df.drop(df.columns[0], axis=1)

df.columns.name = None # Remove the column name

df.reset_index(drop=True, inplace=True) # remove the index column
df.to_csv('Kenya World Bank Data (2013-2022).csv', index=False)

