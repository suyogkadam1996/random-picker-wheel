import streamlit as st
import random
import time
import json
import streamlit.components.v1 as components

# Streamlit Page Config
st.set_page_config(page_title="Random Picker Wheel", page_icon="🎡", layout="wide")

st.title("🎡 Random Person Picker Wheel")

col1, col2 = st.columns([2, 3])  # Adjust the ratio to control layout

with col2:
    st.subheader("Enter names (one per line):")
    names_input = st.text_area("", height=200)
    if st.button("✅ Add These Names"):
        st.session_state.names = names_input.split("\n")
        st.session_state.names = [name.strip() for name in st.session_state.names if name.strip()]
        st.rerun()
    if st.button("🔄 Restart Wheel"):
        st.session_state.clear()
        st.rerun()

if "names" not in st.session_state:
    st.session_state.names = []

names = st.session_state.names

# JavaScript code for spinning wheel with fast initial spin and slow down, removing pointer
wheel_html = """
<!DOCTYPE html>
<html>
<head>
    <script>
        let names = [];
        let angle = 0;
        let spinning = false;
        let winnerIndex = null;

        function setNames(newNames) {
            names = newNames;
            drawWheel();
        }

        function drawWheel() {
            let canvas = document.getElementById("wheelCanvas");
            let ctx = canvas.getContext("2d");
            let totalSlices = names.length;
            let startAngle = 0;
            let arc = 2 * Math.PI / totalSlices;
            let colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#FFC300", "#6A0572"];
            let fontSize = Math.max(10, 40 - totalSlices);
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.font = fontSize + "px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            for (let i = 0; i < totalSlices; i++) {
                let sliceAngle = startAngle + i * arc;
                ctx.fillStyle = colors[i % colors.length];
                ctx.beginPath();
                ctx.moveTo(200, 200);
                ctx.arc(200, 200, 200, sliceAngle, sliceAngle + arc, false);
                ctx.lineTo(200, 200);
                ctx.fill();
                ctx.save();
                ctx.fillStyle = "white";
                ctx.translate(200 + Math.cos(sliceAngle + arc / 2) * 140, 200 + Math.sin(sliceAngle + arc / 2) * 140);
                ctx.rotate(sliceAngle + arc / 2);
                ctx.fillText(names[i], 0, 0);
                ctx.restore();
            }
        }

        function spinWheel() {
            if (spinning) return;
            spinning = true;
            let totalSlices = names.length;
            let arc = 2 * Math.PI / totalSlices;
            winnerIndex = Math.floor(Math.random() * totalSlices);
            let winnerAngle = (2 * Math.PI) - (winnerIndex * arc + arc / 2);
            let spinTime = 4000;
            let start = Date.now();

            function animate() {
                let elapsed = Date.now() - start;
                if (elapsed < spinTime) {
                    let progress = elapsed / spinTime;
                    let speedFactor = (1 - progress) * 10; // Fast at start, slow at end
                    angle += speedFactor * 0.1;
                    let canvas = document.getElementById("wheelCanvas");
                    let ctx = canvas.getContext("2d");
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.save();
                    ctx.translate(200, 200);
                    ctx.rotate(angle);
                    ctx.translate(-200, -200);
                    drawWheel();
                    ctx.restore();
                    requestAnimationFrame(animate);
                } else {
                    spinning = false;
                    let selectedName = names[winnerIndex];
                    document.getElementById("result").innerHTML = "<h1 style='color: red; font-size: 40px; animation: flash 1s infinite alternate;'>🎉 " + selectedName + " 🎉</h1>";
                }
            }
            animate();
        }
    </script>
    <style>
        @keyframes flash {
            from {opacity: 1;}
            to {opacity: 0.5;}
        }
    </style>
</head>
<body onload="drawWheel()">
    <canvas id="wheelCanvas" width="400" height="400"></canvas>
    <br>
    <button onclick="spinWheel()" style="padding: 10px 20px; font-size: 16px;">Click to Spin</button>
    <h2 id="result" style="color: red; font-size: 24px; margin-top: 20px; text-align: center; white-space: nowrap;">🎉 Winner: 🎉</h2>
</body>
</html>
"""

with col1:
    if names:
        names_json = json.dumps(names)
        wheel_html = wheel_html.replace("let names = [];", f"let names = {names_json};")
        components.html(wheel_html, height=550)
    else:
        st.warning("⚠️ Please enter at least one name to start.")
        