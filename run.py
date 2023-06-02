import subprocess
import os
from pathlib import Path

def run():
    """ runs the app.py file within the set up virtual environment
    """

    # find the base path and set path to python binary
    base_path = Path(__file__).parent
    python_bin = f"{base_path}/venv/Scripts/python" if os.name == 'nt' else f"{base_path}/venv/bin/python3"

    cmd = f"{python_bin} app.py"
    process = subprocess.Popen(cmd, shell=True) 
    process.wait()
    # kill the process
    process.kill()


if __name__ == '__main__':
    run()    