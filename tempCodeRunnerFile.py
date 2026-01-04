import subprocess
import sys

print("✋ Starting AirDraw 3D...")
print("Draw using your hand. Press ESC when done.")

# Run drawing phase
subprocess.run([sys.executable, "main.py"])

print("🧊 Opening 3D Viewer...")
# Run 3D viewer
subprocess.run([sys.executable, "viewer_3d.py"])
