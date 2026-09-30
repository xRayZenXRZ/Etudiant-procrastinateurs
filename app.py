import streamlit as st
import uuid
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. Authenticate with Google Sheets using Streamlit Secrets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
client = gspread.authorize(creds)

# 2. Open the specific Google Sheet (make sure the name matches exactly)
sheet = client.open("Experiment_Data").sheet1

# 3. Initialize the SID and Form assignment
if 'sid' not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())[:8].upper()
    st.session_state.condition = random.choice(["Form A", "Form B"])

st.title("Experiment Study")
st.divider()

# 4. Route the user and save data upon submission
if st.session_state.condition == "Form A":
    st.header("Condition A")
    
    with st.form("form_a"):
        response = st.slider("How would you rate this experience?", 1, 10)
        
        if st.form_submit_button("Submit"):
            # Append the data directly as a new row in Google Sheets
            sheet.append_row([
                st.session_state.sid, 
                st.session_state.condition, 
                response, 
                str(datetime.now())
            ])
            st.success("Thank you! Your response has been recorded.")

elif st.session_state.condition == "Form B":
    st.header("Condition B")
    
    with st.form("form_b"):
        response = st.radio("Choose your preference:", ["Option 1", "Option 2"])
        
        if st.form_submit_button("Submit"):
            # Append the data directly as a new row in Google Sheets
            sheet.append_row([
                st.session_state.sid, 
                st.session_state.condition, 
                response, 
                str(datetime.now())
            ])
            st.success("Thank you! Your response has been recorded.")