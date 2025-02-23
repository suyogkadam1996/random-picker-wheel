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

if "names" not in st.session_state:
    st.session_state.names = []

names = st.session_state.names

# JavaScript code for spinning wheel
wheel_html = """
<!DOCTYPE html>
<html>
<head>
    <script>
        let names = [];
        let angle = 0;
        let spinning = false;

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
                let angle = startAngle + i * arc;
                ctx.fillStyle = colors[i % colors.length];
                ctx.beginPath();
                ctx.moveTo(200, 200);
                ctx.arc(200, 200, 200, angle, angle + arc, false);
                ctx.lineTo(200, 200);
                ctx.fill();
                ctx.save();
                ctx.fillStyle = "white";
                ctx.translate(200 + Math.cos(angle + arc / 2) * 140, 200 + Math.sin(angle + arc / 2) * 140);
                ctx.rotate(angle + arc / 2);
                ctx.fillText(names[i], 0, 0);
                ctx.restore();
            }
            drawPointer();
        }

        function drawPointer() {
            let canvas = document.getElementById("wheelCanvas");
            let ctx = canvas.getContext("2d");
            ctx.fillStyle = "black";
            ctx.beginPath();
            ctx.moveTo(195, 10);
            ctx.lineTo(205, 10);
            ctx.lineTo(200, 30);
            ctx.fill();
        }

        function spinWheel() {
            if (spinning) return;
            spinning = true;
            let canvas = document.getElementById("wheelCanvas");
            let ctx = canvas.getContext("2d");
            let totalSlices = names.length;
            let arc = 2 * Math.PI / totalSlices;
            let spinTime = 3000;
            let start = Date.now();

            function animate() {
                let elapsed = Date.now() - start;
                if (elapsed < spinTime) {
                    angle += (spinTime - elapsed) / 200;
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
                    let selectedIndex = Math.floor(((angle % (2 * Math.PI)) / arc + totalSlices) % totalSlices);
                    let selectedName = names[selectedIndex];
                    document.getElementById("result").innerText = "🎉 Winner: " + selectedName + " 🎉";
                }
            }
            animate();
        }
    </script>
</head>
<body onload="drawWheel()">
    <canvas id="wheelCanvas" width="400" height="400"></canvas>
    <br>
    <button onclick="spinWheel()" style="padding: 10px 20px; font-size: 16px;">Click to Spin</button>
    <h2 id="result" style="color: red; margin-top: 20px;"></h2>
</body>
</html>
"""

with col1:
    if names:
        names_json = json.dumps(names)
        wheel_html = wheel_html.replace("let names = [];", f"let names = {names_json};")
        components.html(wheel_html, height=500)
    else:
        st.warning("⚠️ Please enter at least one name to start.")
