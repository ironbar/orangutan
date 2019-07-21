import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.remove(os.path.join(SCRIPT_DIR, 'summary.json'))
frames = glob.glob(os.path.join(SCRIPT_DIR, 'frames', '*.npz'))
[os.remove(frame) for frame in frames]