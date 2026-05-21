import sys
import os
import subprocess

subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'app', 'main.py')])