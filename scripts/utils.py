import subprocess
import os

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Error running command: {command}\n{result.stderr}")
    else:
        log(result.stdout)
    return result.returncode
