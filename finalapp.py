import streamlit as st
import pickle

# Load the trained Random Forest model
try:
    pickle_in = open('rfmodel.pkl', 'rb') 
    classifier = pickle.load(pickle_in)
except FileNotFoundError:
    st.error("Error: Unable to load the trained model. Make sure 'rfmodel.pkl' exists in the current directory.")
    
def prediction(features):
    try:
        # Making predictions 
        Credit_Score = classifier.predict([features])[0]  # Assuming credit score is the only prediction output
        return Credit_Score, None
    except Exception as e:
        return None, f"Error occurred while making prediction: {e}"

def categorize_credit_score(Credit_Score):
    if Credit_Score == 1:
        return "Bad"
    elif Credit_Score == 2:
        return "Standard"
    elif Credit_Score == 3:
        return "Good"
    else:
        return "Unknown"

def main():
    # Front end elements of the web page
    st.title('Credit Score Prediction App')

    # Add inputs for user to enter data
    age = st.slider("Age", min_value=0, max_value=100, step=1)
    annual_income = st.number_input("Annual Income")
    delay_from_due_date = st.number_input("Delay from Due Date")
    num_of_delayed_payment = st.number_input("Number of Delayed Payments", min_value=0, max_value=100, step=1)
    outstanding_debt = st.number_input("Outstanding Debt")
    credit_history_age = st.number_input("Credit History Age")
    payment_of_min_amount = st.selectbox("Payment of Minimum Amount", ['Yes', 'No'])
    total_emi_per_month = st.number_input("Total EMI per Month")
    payment_behaviour = st.slider("Payment Behaviour", min_value=1, max_value=6, step=1)
    monthly_balance = st.number_input("Monthly Balance")
    
    # Get the selected occupation
    occupation_options = ['Accountant', 'Architect', 'Developer', 'Doctor', 'Engineer',
                          'Entrepreneur', 'Journalist', 'Lawyer', 'Manager', 'Mechanic',
                          'MediaManager', 'Musician', 'Scientist', 'Teacher', 'Writer']
    Occupation = st.selectbox('Occupation', occupation_options)

    # Convert Occupation to one-hot encoding
    occupation_encoded = [0] * len(occupation_options)
    occupation_index = occupation_options.index(Occupation)
    occupation_encoded[occupation_index] = 1

    # Convert payment_of_min_amount to numerical value
    payment_of_min_amount_numeric = 1 if payment_of_min_amount == 'Yes' else 0
    
    # When 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        features = [age, annual_income, delay_from_due_date, num_of_delayed_payment,
                    outstanding_debt, credit_history_age, payment_of_min_amount_numeric,
                    total_emi_per_month, payment_behaviour, monthly_balance]
        features.extend(occupation_encoded)
        Credit_Score, error_message = prediction(features)
        if error_message:
            st.error(error_message)
        else:
            credit_score_category = categorize_credit_score(Credit_Score)
            st.write(f"Predicted Credit Score: {credit_score_category}")

if __name__ == '__main__':
    main()
