
import streamlit as st
import uuid
import random

# 1. Initialize the SID and Form assignment on the first run only
if 'sid' not in st.session_state:
    # Generate a random 8-character Subject ID
    st.session_state.sid = str(uuid.uuid4())[:8].upper()
    
    # Randomly assign the condition (50/50 split)
    st.session_state.condition = random.choice(["Form A", "Form B"])

# Display the participant info (optional, usually hidden in real experiments)
st.sidebar.write(f"**Participant SID:** {st.session_state.sid}")
st.sidebar.write(f"**Assigned:** {st.session_state.condition}")

st.title("Experiment Study")
st.divider()

# 2. Route the user to the correct form based on their session state
if st.session_state.condition == "Form A":
    st.header("Condition A")
    
    with st.form("form_a"):
        st.write("Welcome to the first version of the task.")
        response = st.slider("How would you rate this experience?", 1, 10)
        
        # Submit button for Form A
        if st.form_submit_button("Submit"):
            st.success(f"Data saved for {st.session_state.sid} (Form A)")
            # Add your database saving logic here

elif st.session_state.condition == "Form B":
    st.header("Condition B")
    
    with st.form("form_b"):
        st.write("Welcome to the alternative version of the task.")
        response = st.radio("Choose your preference:", ["Option 1", "Option 2"])
        
        # Submit button for Form B
        if st.form_submit_button("Submit"):
            st.success(f"Data saved for {st.session_state.sid} (Form B)")
            # Add your database saving logic here