import subprocess
import time
import webbrowser
import os
import sys

def main():
    print("===================================")
    print("  CHIMERA Studio - Boot Sequence  ")
    print("===================================")
    
    # Ensure dependencies are installed
    print("[1] Verifying dependencies (fastapi, uvicorn)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "-q"])
    
    # Start the API server in a subprocess
    print("[2] Initializing API Server...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.server:app", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Wait a second for the server to spin up
    time.sleep(2)
    
    # Open the browser
    print("[3] Launching Studio Interface...")
    webbrowser.open("http://127.0.0.1:8000")
    
    print("\nCHIMERA is running! Close this window to shut down the server.")
    
    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down CHIMERA...")
        api_process.terminate()

if __name__ == "__main__":
    main()
