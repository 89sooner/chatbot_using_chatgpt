# run.py

import subprocess

if __name__ == "__main__":
    # Create two subprocesses for each script
    proc1 = subprocess.Popen(["python", "main.py"])
    proc2 = subprocess.Popen(["python", "slack_service.py"])

    # Wait for both subprocesses to finish
    proc1.wait()
    proc2.wait()
