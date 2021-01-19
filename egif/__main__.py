import os
import sys
from pathlib import Path

MAIN_DIR = Path(__file__).parent.parent.absolute()
sys.path.append(str(MAIN_DIR.absolute()))


import argparse
from egif import run_app


parser = argparse.ArgumentParser(description='Egif image viewer.')
parser.add_argument('file', help='File to open.')

args = parser.parse_args()
run_app(args.file)
