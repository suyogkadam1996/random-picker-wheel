import streamlit as st
import random
import time

st.title("🎡 Random Person Picker Wheel")

# User input for team members
names = st.text_area("Enter names (one per line):").split("\n")
names = [name.strip() for name in names if name.strip()]

if names:
    if st.button("🎰 Spin the Wheel"):
        with st.spinner("Spinning the wheel..."):
            time.sleep(2)  # Simulating wheel spinning effect
            chosen_name = random.choice(names)
        
        st.success(f"🎉 The selected person is: **{chosen_name}**")
else:
    st.warning("Please enter at least one name to start.")
