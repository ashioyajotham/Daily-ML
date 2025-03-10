import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, List
import logging

# 1. Time Series Data Cleaning
def clean_timeseries_data(df: pd.DataFrame, 
                         date_col: str,
                         value_cols: List[str]) -> pd.DataFrame:
    """
    Clean time series data by handling missing values, outliers, and ensuring proper datetime format.
    
    Parameters:
    df: Input DataFrame with time series data
    date_col: Name of the datetime column
    value_cols: List of columns containing numeric values to clean
    """
    # Copy input data
    df = df.copy()
    
    # Convert to datetime
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Sort by date
    df = df.sort_values(date_col)
    
    # Set datetime as index
    df.set_index(date_col, inplace=True)
    
    for col in value_cols:
        # Handle outliers using IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower_bound, upper_bound)
        
        # Interpolate missing values
        df[col] = df[col].interpolate(method='time')
    
    # Resample to ensure regular intervals (e.g., hourly)
    df = df.resample('H').mean()
    
    return df

# 2. Customer Survey Data Cleaning
def clean_survey_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean survey data by standardizing responses, handling text fields,
    and managing categorical variables.
    """
    df = df.copy()
    
    # Standardize text responses
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        # Convert to lowercase and strip whitespace
        df[col] = df[col].str.lower().str.strip()
        
        # Remove special characters
        df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
    
    # Handle categorical variables
    categorical_cols = ['gender', 'age_group', 'satisfaction']
    for col in categorical_cols:
        if col in df.columns:
            # Fill missing with mode
            df[col] = df[col].fillna(df[col].mode()[0])
    
    # Convert numeric ratings to float
    rating_cols = [col for col in df.columns if 'rating' in col.lower()]
    for col in rating_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Scale ratings to 0-1
        df[col] = df[col] / df[col].max()
    
    return df

# 3. Transaction Data Cleaning
def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean financial transaction data by handling duplicates, 
    standardizing currencies, and validating amounts.
    """
    df = df.copy()
    
    # Remove duplicate transactions
    df = df.drop_duplicates(subset=['transaction_id', 'date', 'amount'])
    
    # Convert all amounts to same currency (assuming USD)
    currency_rates = {
        'EUR': 1.1,
        'GBP': 1.3,
        'JPY': 0.009
    }
    
    def standardize_amount(row):
        if row['currency'] in currency_rates:
            return row['amount'] * currency_rates[row['currency']]
        return row['amount']
    
    df['amount_usd'] = df.apply(standardize_amount, axis=1)
    
    # Validate and clean dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    
    # Remove transactions with invalid amounts
    df = df[df['amount_usd'] > 0]
    
    return df

# 4. Sensor Data Cleaning
def clean_sensor_data(df: pd.DataFrame,
                     sensor_cols: List[str],
                     rolling_window: int = 5) -> pd.DataFrame:
    """
    Clean IoT sensor data by handling noise, gaps, and calibration issues.
    """
    df = df.copy()
    
    for col in sensor_cols:
        # Remove physically impossible values
        df[col] = df[col].clip(lower=0)
        
        # Smooth noisy data with rolling mean
        df[f'{col}_smooth'] = df[col].rolling(
            window=rolling_window, 
            center=True
        ).mean()
        
        # Detect and handle sudden spikes
        rolling_std = df[col].rolling(window=rolling_window).std()
        df[col] = np.where(
            df[col] > (df[f'{col}_smooth'] + 2 * rolling_std),
            df[f'{col}_smooth'],
            df[col]
        )
        
        # Fill missing values with forward fill (assume last known value)
        df[col] = df[col].fillna(method='ffill')
    
    return df

# 5. Text Data Cleaning
def clean_text_data(df: pd.DataFrame,
                   text_columns: List[str]) -> pd.DataFrame:
    """
    Clean text data by standardizing format, removing unwanted characters,
    and handling common text issues.
    """
    df = df.copy()
    
    for col in text_columns:
        # Convert to string type
        df[col] = df[col].astype(str)
        
        # Remove URLs
        df[col] = df[col].apply(
            lambda x: re.sub(r'http\S+|www.\S+', '', x)
        )
        
        # Remove special characters and numbers
        df[col] = df[col].apply(
            lambda x: re.sub(r'[^\w\s]', '', x)
        )
        
        # Standardize whitespace
        df[col] = df[col].apply(
            lambda x: ' '.join(x.split())
        )
        
        # Convert to lowercase
        df[col] = df[col].str.lower()
        
        # Remove empty strings
        df[col] = df[col].replace('', np.nan)
    
    return df

# Example usage for all scripts
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Example for time series data
        ts_data = pd.read_csv('timeseries.csv')
        clean_ts = clean_timeseries_data(
            ts_data, 
            'timestamp',
            ['temperature', 'humidity']
        )
        
        # Example for survey data
        survey_data = pd.read_csv('survey.csv')
        clean_survey = clean_survey_data(survey_data)
        
        # Example for transaction data
        transaction_data = pd.read_csv('transactions.csv')
        clean_transactions = clean_transaction_data(transaction_data)
        
        # Example for sensor data
        sensor_data = pd.read_csv('sensor.csv')
        clean_sensors = clean_sensor_data(
            sensor_data,
            ['pressure', 'vibration', 'temperature']
        )
        
        # Example for text data
        text_data = pd.read_csv('text.csv')
        clean_text = clean_text_data(
            text_data,
            ['comments', 'descriptions']
        )
        
        logging.info("All data cleaning completed successfully")
        
    except Exception as e:
        logging.error(f"Error during data cleaning: {str(e)}")
