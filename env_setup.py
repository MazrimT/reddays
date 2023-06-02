import subprocess
import os
import sys
from pathlib import Path
import shutil

def run_setup():
    """ sets up a base project
    Creates a virtual environment.
    Uppgrades pip
    Installs wheel
    Installs anything the requirements.txt file
    """

    # find the base path and set path to python binary
    base_path = Path(__file__).parent
    python_bin = f"{base_path}/venv/Scripts/python" if os.name == 'nt' else f"{base_path}/venv/bin/python3"    

    if Path(f"{base_path}/venv").exists():
        print("Virtual Environment already exists what should we do?")
        print("d: Delete if exists and recreate it (default)")
        print("n: do nothing and stop the script")
        print("r: run the installs anyway without deleting first")

        answer = input("d/n/r (d): ") or 'd'
    
    
    if answer.upper() == 'N':
        print("Exiting")
        sys.exit()
    
    elif answer.upper() == 'D':
        print("Deleting and recreating")
        shutil.rmtree(f"{base_path}/venv", ignore_errors=True)

        # create virtual environment if not exists
        make_venv = "python -m venv venv"
        os.system(make_venv)
    
    elif answer.upper() == 'R':
        print("Running anyway")


    # commands to run
    cmds = [
        '-m pip install --upgrade pip',
        '-m pip install wheel',
        '-m pip install -r requirements.txt',
    ]

    for cmd in cmds:

        cmd = [python_bin] + cmd.split()
        print(' '.join(cmd))
        process = subprocess.Popen(cmd, shell=True) 
        # wait for process to run
        process.wait()
        # kill the process
        process.kill()


if __name__ == '__main__':
    run_setup()