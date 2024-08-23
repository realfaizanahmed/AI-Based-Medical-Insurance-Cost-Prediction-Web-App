import streamlit as st
import requests

# FastAPI backend URL
API_URL = "https://realfaizanahmed.github.io/AI-Based-Medical-Insurance-Cost-Prediction-Web-App/"

# Streamlit App Title
st.title("Medical Insurance Cost Prediction App")
st.write("Use the sidebar to enter your details and click 'Predict' to see your medical insurance cost prediction:")

# Sidebar for User Input
st.sidebar.header("Enter Your Details")

# Collect all user inputs within a form
with st.sidebar.form("prediction_form"):
    age = st.number_input("Age", min_value=0, max_value=100, value=25, help="Enter your age")
    bmi = st.number_input("BMI", min_value=0.0, max_value=60.0, value=25.0, help="Enter your Body Mass Index")
    children = st.number_input("Number of Children", min_value=0, max_value=10, value=0, help="Enter the number of children")
    sex = st.selectbox("Sex", options=['male', 'female'], help="Select your sex")
    smoker = st.selectbox("Smoker", options=['yes', 'no'], help="Do you smoke?")
    region = st.selectbox("Region", options=['northeast', 'northwest', 'southeast', 'southwest'], help="Select your region")

    # Add a submit button inside the form
    submitted = st.form_submit_button("Predict")

# Prediction Logic after form submission
if submitted:
    user_input = {
        'age': age,
        'bmi': bmi,
        'children': children,
        'sex': sex,
        'smoker': smoker,
        'region': region
    }

    # Send data to FastAPI backend
    try:
        response = requests.post(API_URL, json=user_input)
        response_data = response.json()

        if "predicted_cost" in response_data:
            predicted_cost = response_data.get("predicted_cost", 0)
            mse = float(response_data.get("mse", 0))
            mae = float(response_data.get("mae", 0))
            rmse = float(response_data.get("rmse", 0))
            r2 = float(response_data.get("r2", 0))

            # Display the Result
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; background-color: #d4edda; padding: 10px; border-radius: 5px; border: 1px solid #c3e6cb;">
                    <h3 style="color: #155724;">Predicted Insurance Cost: ${predicted_cost:.2f}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Display Model Performance Metrics
            st.write("### Model Performance Metrics")
            st.write(f"- **Mean Squared Error (MSE)**: {mse:.2f}")
            st.write(f"- **Mean Absolute Error (MAE)**: {mae:.2f}")
            st.write(f"- **Root Mean Squared Error (RMSE)**: {rmse:.2f}")
            st.write(f"- **R-squared (R²)**: {r2:.2f}")

        else:
            st.write("Error: ", response_data.get("error", "Unknown error"))

    except requests.exceptions.RequestException as e:
        st.write(f"Request failed: {e}")
