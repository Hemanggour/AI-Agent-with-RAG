import argparse
import subprocess
import time

from pyngrok import ngrok


def run_backend():
    print("Starting FastAPI backend on http://localhost:8000 ...")
    return subprocess.Popen(["uvicorn", "backend.main:app", "--port", "8000"])


def run_frontend_online():
    print("tarting Streamlit frontend with ngrok tunnel...")
    public_url = ngrok.connect(8501)
    print(f"Public Streamlit URL: {public_url}")
    time.sleep(1)
    return subprocess.Popen(["streamlit", "run", "frontend/app.py"])


def run_frontend_local():
    print("Starting Streamlit frontend locally on http://localhost:8501 ...")
    return subprocess.Popen(
        ["streamlit", "run", "frontend/app.py", "--server.port", "8501"]
    )


def main():
    parser = argparse.ArgumentParser(description="Launch AI Assistant App")
    parser.add_argument(
        "--online", action="store_true", help="Run frontend using ngrok"
    )
    args = parser.parse_args()

    # Start backend
    backend_proc = run_backend()

    # Wait to avoid race condition
    time.sleep(2)

    # Start frontend
    if args.online:
        frontend_proc = run_frontend_online()
    else:
        frontend_proc = run_frontend_local()

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()


if __name__ == "__main__":
    main()
