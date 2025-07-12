import os
from dotenv import load_dotenv
import subprocess

from pyngrok import ngrok
from pyngrok.conf import PyngrokConfig

load_dotenv()

# Start ngrok tunnel
pyngrok_config = PyngrokConfig(auth_token=os.getenv("NGROK_AUTHTOKEN"))
public_url = ngrok.connect(8501, pyngrok_config=pyngrok_config)
print("Streamlit is live at:", public_url)

# Launch Streamlit app
subprocess.run(["streamlit", "run", "frontend/app.py"])
