🖌️ AirDraw 3D

Draw in mid-air using your hand gestures and visualize in true 3D!
Experience gesture-based drawing, instant 3D extrusion, and export your creations.

🎯 Features

Hand-gesture drawing: Draw naturally with your index finger in front of your webcam.

3D strokes: Capture depth (Z-axis) for immersive 3D visualization.

Instant palm extrusion: Open your palm to extrude strokes in 3D while drawing.

Multiple colors & eraser: Use your thumb to select color palettes while drawing.

Smooth strokes: Stabilized drawing using averaging for natural lines.

Export drawings:

2D Image (airdraw_2d.png)

3D JSON data (airdraw_3d.json)

3D Viewer: See your strokes in 3D space with PyVista.

Keyboard controls:

ESC: Exit

Open palm: 3D conversion

Fist: Stop drawing

🖥️ Demo

🎥 Instagram-style demo: Link to Reel

(Optional: Add GIF of the app running locally)

🚀 Installation

Requirements:

Python ≥ 3.13

OpenCV

Mediapipe Tasks

Numpy

PyVista

Install dependencies:
pip install opencv-python mediapipe numpy pyvista


⚠️ Make sure your Python version is 3.13+ to avoid mp.solutions issues.

🏃 Usage

Clone the repo:

git clone https://github.com/<your-username>/airdraw-3d.git
cd airdraw-3d


Run the app:

python run.py


This runs drawing (main.py) and then 3D viewer (viewer_3d.py) automatically.

📁 File Structure
AirDraw-3D/
├─ main.py           # Hand gesture drawing
├─ viewer_3d.py      # 3D stroke visualization
├─ run.py            # Starts drawing + viewer
├─ hand_landmarker.task  # Mediapipe hand model
├─ README.md
├─ airdraw_2d.png    # Generated 2D image
└─ airdraw_3d.json   # Generated 3D strokes

🎨 How it Works

Draw: Move your index finger to draw in the air.

Change colors: Use your thumb on the circular palette to select colors.

Stop drawing: Make a fist to end the current stroke.

3D conversion: Open your palm to extrude strokes in 3D.

View in 3D: The viewer loads strokes from airdraw_3d.json for an immersive 3D display.

Download: Drawing saved automatically as PNG and JSON.

🔧 Customization

Add new colors in main.py under palette.

Adjust smoothing by changing the deque(maxlen=5) length.

Modify stroke thickness based on depth (tip.z).

🏆 Roadmap

Export as .OBJ / .GLB for 3D printing or Blender import.

Live collaboration & cloud sync.

VR/AR integration.

Aesthetic UI for palette & 3D interaction.
