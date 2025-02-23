import streamlit as st
import random
import time
from streamlit_extras import add_vertical_space

st.set_page_config(page_title="Random Picker Wheel", page_icon="🎡", layout="centered")

st.title("🎡 Random Person Picker Wheel")

# User input for team members
names = st.text_area("Enter names (one per line):").split("\n")
names = [name.strip() for name in names if name.strip()]

st.markdown("---")

# Button to start spinning
if names:
    if st.button("🎰 Spin the Wheel"):
        with st.spinner("Spinning the wheel..."):
            spin_duration = 3  # Total time to simulate spinning
            final_choice = None
            
            for i in range(30):  # Simulate the wheel slowing down
                selected = random.choice(names)
                st.subheader(f"🎡 Spinning... {selected}")
                time.sleep(spin_duration / (i + 10))  # Slow down effect
            
            final_choice = selected
            
        # Display the final choice
        st.balloons()  # Celebration effect
        st.success(f"🎉 The selected person is: **{final_choice}**")

        # Confetti effect (Requires streamlit-extras)
        from streamlit_extras.stylable_container import stylable_container
        with stylable_container(
            key="confetti", css_styles="animation: pop 0.5s ease-in-out infinite alternate;"
        ):
            st.markdown(f"<h2 style='text-align: center; color: #ff5733;'>🎊 {final_choice} 🎊</h2>", unsafe_allow_html=True)

else:
    st.warning("⚠️ Please enter at least one name to start.")
