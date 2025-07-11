from pyngrok import ngrok
import subprocess

# Start ngrok tunnel
public_url = ngrok.connect(8501)
print("Streamlit is live at:", public_url)

# Launch Streamlit app
subprocess.run(["streamlit", "run", "frontend/app.py"])
