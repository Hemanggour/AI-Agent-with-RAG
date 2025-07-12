import subprocess

from pyngrok import ngrok

# Start ngrok tunnel
public_url = ngrok.connect(8501, authtoken_from_env=True)
print("Streamlit is live at:", public_url)

# Launch Streamlit app
subprocess.run(["streamlit", "run", "frontend/app.py"])
