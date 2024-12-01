import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load the models
rf_model = joblib.load('random_forest_model.pkl')
gbm_model = joblib.load('gradient_boosting_model.pkl')
lr_model = joblib.load('logistic_regression_model.pkl')
svm_model = joblib.load('svm_model.pkl')

# Title of the app
st.title("Cognitive Decline Prediction App")
st.write("""
This application predicts cognitive decline based on various health-related features.
You can choose a model and input the necessary features to get predictions.
""")

# Sidebar for user input
st.sidebar.header("User Input Features")

def user_input_features():
    year = st.sidebar.number_input("Year", min_value=2011, max_value=2023, value=2021)
    location_abbr = st.sidebar.selectbox("Location Abbreviation", ["AL", "AK", "AZ", "AR", "CA"])  # Add more as needed
    class_type = st.sidebar.selectbox("Class", ["Alcohol Consumption", "Health", "Other"])  # Add more as needed
    data_value = st.sidebar.number_input("Data Value", min_value=0.0, max_value=100.0, value=50.0)
    response = st.sidebar.selectbox("Response", ["yes", "no", "unknown", "other"])  # Add more as needed
    # Add more features as needed
    return pd.DataFrame([[year, location_abbr, class_type, data_value, response]], 
                        columns=["Year", "Locationabbr", "Class", "Data_value", "Response"])

input_data = user_input_features()

# Model selection
model_choice = st.sidebar.selectbox("Select Model", ["Random Forest", "Gradient Boosting", "Logistic Regression", "SVM"])

# Prediction
if st.sidebar.button("Predict"):
    if model_choice == "Random Forest":
        prediction = rf_model.predict(input_data)
    elif model_choice == "Gradient Boosting":
        prediction = gbm_model.predict(input_data)
    elif model_choice == "Logistic Regression":
        prediction = lr_model.predict(input_data)
    elif model_choice == "SVM":
        prediction = svm_model.predict(input_data)

    st.write(f"Prediction: {prediction[0]}")

# Footer
st.write("""
### About
This application uses machine learning models to predict cognitive decline based on user input features. 
The models have been trained on health-related data and can provide insights based on the selected features.
""")