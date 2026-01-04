# # # # import json
# # # # import pyvista as pv
# # # # import numpy as np

# # # # # ---------------- LOAD DATA ----------------
# # # # with open("strokes_3d.json") as f:
# # # #     strokes = json.load(f)

# # # # plotter = pv.Plotter()
# # # # plotter.background_color = "white"

# # # # # ---------------- EXTRUDE STROKES ----------------
# # # # for stroke in strokes:
# # # #     pts = np.array(stroke["points"])
# # # #     color = stroke["color"]
# # # #     # Normalize color to 0-1 for pyvista
# # # #     color_norm = np.array(color)/255
# # # #     for i in range(1, len(pts)):
# # # #         x1, y1, z1 = pts[i-1]
# # # #         x2, y2, z2 = pts[i]
# # # #         line = pv.Line([x1, y1, -z1*500], [x2, y2, -z2*500])
# # # #         plotter.add_mesh(line, color=color_norm, line_width=5)

# # # # plotter.show_grid()
# # # # plotter.show()
# # # import json
# # # import numpy as np
# # # import pyvista as pv

# # # with open("strokes_3d.json") as f:
# # #     strokes = json.load(f)

# # # plotter = pv.Plotter()
# # # plotter.set_background("black")

# # # for stroke in strokes:
# # #     pts = np.array(stroke["points"])
# # #     color = np.array(stroke["color"]) / 255.0

# # #     spline = pv.Spline(pts, len(pts) * 3)
# # #     plotter.add_mesh(
# # #         spline.tube(radius=0.8),
# # #         color=color
# # #     )

# # # plotter.show()
# # import pyvista as pv
# # import json
# # import numpy as np

# # pv.global_theme.allow_empty_mesh = True

# # with open("strokes.json") as f:
# #     strokes = json.load(f)

# # plotter = pv.Plotter()
# # plotter.set_background("#0f0f1a")  # aesthetic dark

# # for stroke in strokes:
# #     pts = np.array(stroke["points"])
# #     if len(pts) < 2:
# #         continue  # 🔥 FIX: skip empty strokes

# #     spline = pv.Spline(pts, len(pts) * 10)
# #     tube = spline.tube(radius=1.2)

# #     plotter.add_mesh(
# #         tube,
# #         color=[c / 255 for c in stroke["color"]],
# #         smooth_shading=True
# #     )

# # plotter.show_grid(False)
# # plotter.show()
# import json
# import os
# import numpy as np
# import pyvista as pv

# # ---------------- SAFE LOAD ----------------
# if not os.path.exists("strokes_3d.json"):
#     print("❌ strokes_3d.json not found")
#     exit()

# with open("strokes_3d.json", "r") as f:
#     content = f.read().strip()
#     if not content:
#         print("❌ strokes_3d.json is empty")
#         exit()
#     strokes = json.loads(content)

# plotter = pv.Plotter()
# plotter.set_background("black")

# # ---------------- DRAW ----------------
# for stroke in strokes:
#     if len(stroke) < 2:
#         continue

#     pts = np.array(stroke)
#     spline = pv.Spline(pts, len(pts) * 10)
#     tube = spline.tube(radius=1.0)

#     if tube.n_points > 0:
#         plotter.add_mesh(tube, color="cyan")

# plotter.show()
import json
import numpy as np
import pyvista as pv

with open("strokes_3d.json", "r") as f:
    strokes = json.load(f)

plotter = pv.Plotter()
plotter.set_background("black")

for stroke in strokes:
    if len(stroke) < 2:
        continue

    pts = np.array([[p[0], p[1], p[2]*300] for p in stroke])
    color = tuple(c/255 for c in stroke[0][3])

    spline = pv.Spline(pts, len(pts) * 8)
    tube = spline.tube(radius=1.2)

    if tube.n_points > 0:
        plotter.add_mesh(
            tube,
            color=color,
            smooth_shading=True
        )

plotter.show()
