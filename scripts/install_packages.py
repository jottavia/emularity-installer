from utils import log, run_command

def install_packages():
    log("Updating the system...")
    run_command("apt update && apt upgrade -y")

    log("Installing required packages...")
    run_command("apt install -y apache2 git build-essential python3 python-is-python3 python3-pip unzip curl")
