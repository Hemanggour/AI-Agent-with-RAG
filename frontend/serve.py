from pyngrok import ngrok
import subprocess
import time

# Set your ngrok authtoken (only once, or skip if already set)
# ngrok.set_auth_token("your-token")

# Start ngrok tunnel
public_url = ngrok.connect(8501)
print("🚀 Streamlit is live at:", public_url)

# Wait a second before launching Streamlit (optional safety)
time.sleep(1)

# Launch Streamlit app
subprocess.run(["streamlit", "run", "frontend/app.py"])
