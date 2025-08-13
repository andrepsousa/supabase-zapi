import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(_file_), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
