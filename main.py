# # # import cv2
# # # import mediapipe as mp
# # # import numpy as np
# # # import time
# # # import math
# # # from collections import deque
# # # import json

# # # # ---------------- CAMERA ----------------
# # # cap = cv2.VideoCapture(0)

# # # # ---------------- MEDIAPIPE TASKS ----------------
# # # BaseOptions = mp.tasks.BaseOptions
# # # HandLandmarker = mp.tasks.vision.HandLandmarker
# # # HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# # # VisionRunningMode = mp.tasks.vision.RunningMode

# # # options = HandLandmarkerOptions(
# # #     base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
# # #     running_mode=VisionRunningMode.VIDEO,
# # #     num_hands=1,
# # #     min_hand_detection_confidence=0.7,
# # #     min_hand_presence_confidence=0.7,
# # #     min_tracking_confidence=0.7
# # # )

# # # hand_landmarker = HandLandmarker.create_from_options(options)

# # # # ---------------- CANVAS ----------------
# # # WIDTH, HEIGHT = 640, 480
# # # canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# # # # ---------------- STROKES ----------------
# # # strokes = []
# # # current_stroke = None
# # # smooth_points = deque(maxlen=5)

# # # # ---------------- HELPERS ----------------
# # # def smooth(x, y):
# # #     smooth_points.append((x, y))
# # #     sx = int(sum(p[0] for p in smooth_points) / len(smooth_points))
# # #     sy = int(sum(p[1] for p in smooth_points) / len(smooth_points))
# # #     return sx, sy

# # # def is_fist(lm):
# # #     for tip in [8, 12, 16, 20]:
# # #         if lm[tip].y < lm[tip - 2].y:
# # #             return False
# # #     return True

# # # def is_open_palm(lm):
# # #     for tip in [8, 12, 16, 20]:
# # #         if lm[tip].y > lm[tip - 2].y:
# # #             return False
# # #     return True

# # # # ---------------- MAIN LOOP ----------------
# # # while cap.isOpened():
# # #     ret, frame = cap.read()
# # #     if not ret:
# # #         break

# # #     frame = cv2.flip(frame, 1)
# # #     frame = cv2.resize(frame, (WIDTH, HEIGHT))
# # #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# # #     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
# # #     result = hand_landmarker.detect_for_video(
# # #         mp_image, int(time.time() * 1000)
# # #     )

# # #     if result.hand_landmarks:
# # #         hand = result.hand_landmarks[0]

# # #         index_tip = hand[8]
# # #         x = int(index_tip.x * WIDTH)
# # #         y = int(index_tip.y * HEIGHT)
# # #         z = index_tip.z

# # #         x, y = smooth(x, y)

# # #         # Stop drawing
# # #         if is_fist(hand):
# # #             current_stroke = None
# # #             smooth_points.clear()

# # #         else:
# # #             # Start stroke
# # #             if current_stroke is None:
# # #                 current_stroke = {
# # #                     "points": [],
# # #                     "color": (0, 0, 255)
# # #                 }
# # #                 strokes.append(current_stroke)

# # #             # Depth → thickness
# # #             thickness = int(np.interp(z, [-0.2, 0.1], [15, 2]))
# # #             thickness = max(2, thickness)

# # #             current_stroke["points"].append((x, y, z, thickness))

# # #         cv2.circle(frame, (x, y), 8, (255, 0, 0), -1)

# # #     # ---------------- REDRAW CANVAS ----------------
# # #     canvas[:] = 0
# # #     for stroke in strokes:
# # #         pts = stroke["points"]
# # #         for i in range(1, len(pts)):
# # #             x1, y1, _, t1 = pts[i - 1]
# # #             x2, y2, _, t2 = pts[i]
# # #             cv2.line(canvas, (x1, y1), (x2, y2),
# # #                      stroke["color"], int((t1 + t2) / 2))

# # #     # ---------------- DISPLAY ----------------
# # #     output = cv2.addWeighted(frame, 0.7, canvas, 1, 0)
# # #     cv2.putText(output, "AirDraw 3D | Index: Draw | Fist: Stop",
# # #                 (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# # #     cv2.imshow("AirDraw 3D", output)

# # #     if cv2.waitKey(1) & 0xFF == 27:
# # #         break

# # # # ---------------- SAVE 3D STROKES ----------------
# # # with open("strokes_3d.json", "w") as f:
# # #     json.dump(strokes, f)

# # # cap.release()
# # # cv2.destroyAllWindows()

# # # print("✅ 3D strokes saved successfully")
# # import cv2
# # import mediapipe as mp
# # import numpy as np
# # import json
# # import math

# # cap = cv2.VideoCapture(0)

# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(max_num_hands=1)
# # mp_draw = mp.solutions.drawing_utils

# # strokes = []
# # current_stroke = []
# # current_color = (255, 0, 255)  # default aesthetic color
# # drawing = False
# # palm_open = False

# # # 🎨 Aesthetic palette (cursor-based hover)
# # palette = [
# #     ((255, 105, 180), (50, 50)),   # pink
# #     ((173, 216, 230), (100, 50)),  # pastel blue
# #     ((144, 238, 144), (150, 50)),  # pastel green
# #     ((255, 223, 186), (200, 50)),  # peach
# # ]

# # def dist(a, b):
# #     return math.hypot(a[0] - b[0], a[1] - b[1])

# # while True:
# #     ret, frame = cap.read()
# #     frame = cv2.flip(frame, 1)
# #     h, w, _ = frame.shape

# #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     res = hands.process(rgb)

# #     # 🎨 Draw palette UI
# #     for color, pos in palette:
# #         cv2.circle(frame, pos, 18, color, -1)

# #     if res.multi_hand_landmarks:
# #         hand = res.multi_hand_landmarks[0]
# #         lm = hand.landmark

# #         ix, iy = int(lm[8].x * w), int(lm[8].y * h)   # index
# #         tx, ty = int(lm[4].x * w), int(lm[4].y * h)   # thumb
# #         mx, my = int(lm[12].x * w), int(lm[12].y * h) # middle

# #         # 🟢 Hover palette selection (NO CLICK)
# #         for color, pos in palette:
# #             if dist((ix, iy), pos) < 20:
# #                 current_color = color

# #         # ✏️ Draw with index finger
# #         if dist((ix, iy), (tx, ty)) > 45:
# #             drawing = True
# #             z = 15 if palm_open else 0
# #             current_stroke.append([ix, iy, z])
# #         else:
# #             if drawing and len(current_stroke) > 1:
# #                 strokes.append({
# #                     "points": current_stroke,
# #                     "color": current_color
# #                 })
# #             current_stroke = []
# #             drawing = False

# #         # 🧽 Eraser (middle finger pinch)
# #         if dist((mx, my), (tx, ty)) < 30:
# #             strokes = []

# #         # ✋ Palm open = 3D extrusion
# #         palm_open = lm[0].y > lm[9].y

# #         mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

# #     # 🖍️ Draw strokes
# #     for s in strokes:
# #         for i in range(1, len(s["points"])):
# #             cv2.line(
# #                 frame,
# #                 tuple(s["points"][i-1][:2]),
# #                 tuple(s["points"][i][:2]),
# #                 s["color"],
# #                 4
# #             )

# #     cv2.imshow("AirDraw 3D", frame)

# #     if cv2.waitKey(1) & 0xFF == ord('s'):
# #         with open("strokes.json", "w") as f:
# #             json.dump(strokes, f)
# #         break

# # cap.release()
# # cv2.destroyAllWindows()
# import cv2
# import mediapipe as mp
# import numpy as np
# import time
# import json
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# # ---------------- CAMERA ----------------
# cap = cv2.VideoCapture(0)
# WIDTH, HEIGHT = 640, 480

# # ---------------- MEDIAPIPE TASKS ----------------
# BaseOptions = python.BaseOptions
# HandLandmarker = vision.HandLandmarker
# HandLandmarkerOptions = vision.HandLandmarkerOptions
# VisionRunningMode = vision.RunningMode

# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
#     running_mode=VisionRunningMode.VIDEO,
#     num_hands=1,
#     min_hand_detection_confidence=0.7,
#     min_tracking_confidence=0.7
# )

# landmarker = HandLandmarker.create_from_options(options)

# # ---------------- DATA ----------------
# strokes = []
# current_stroke = []
# drawing = False

# canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# # ---------------- GESTURES ----------------
# def is_fist(lm):
#     for tip in [8, 12, 16, 20]:
#         if lm[tip].y < lm[tip - 2].y:
#             return False
#     return True

# # ---------------- LOOP ----------------
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     frame = cv2.resize(frame, (WIDTH, HEIGHT))
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
#     result = landmarker.detect_for_video(mp_image, int(time.time() * 1000))

#     if result.hand_landmarks:
#         lm = result.hand_landmarks[0]
#         tip = lm[8]

#         x = int(tip.x * WIDTH)
#         y = int(tip.y * HEIGHT)
#         z = float(tip.z)

#         if is_fist(lm):
#             if len(current_stroke) > 1:
#                 strokes.append(current_stroke)
#             current_stroke = []
#             drawing = False
#         else:
#             drawing = True
#             current_stroke.append([x, y, z])
#             cv2.circle(canvas, (x, y), 4, (0, 0, 255), -1)

#     output = cv2.addWeighted(frame, 0.7, canvas, 1, 0)
#     cv2.putText(output,
#         "Index: Draw | Fist: Stop | ESC: Save",
#         (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
#         (0,255,0), 2)

#     cv2.imshow("AirDraw", output)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- SAVE ----------------
# if len(current_stroke) > 1:
#     strokes.append(current_stroke)

# with open("strokes_3d.json", "w") as f:
#     json.dump(strokes, f)

# cap.release()
# cv2.destroyAllWindows()
# print("✅ strokes_3d.json saved successfully")
import cv2
import mediapipe as mp
import numpy as np
import time
import json
import math
from collections import deque
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
WIDTH, HEIGHT = 640, 480

# ---------------- MEDIAPIPE ----------------
BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

# ---------------- CANVAS ----------------
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# ---------------- COLORS (AESTHETIC) ----------------
palette = [
    (255, 80, 255),   # neon pink
    (80, 200, 255),   # cyan
    (120, 255, 120),  # green
    (255, 200, 80),   # gold
    (180, 120, 255),  # purple
]
current_color = palette[0]

# ---------------- STROKES ----------------
strokes = []
current_stroke = []
smooth_points = deque(maxlen=7)

# ---------------- HELPERS ----------------
def smooth(x, y):
    smooth_points.append((x, y))
    sx = int(sum(p[0] for p in smooth_points) / len(smooth_points))
    sy = int(sum(p[1] for p in smooth_points) / len(smooth_points))
    return sx, sy

def is_fist(lm):
    for tip in [8, 12, 16, 20]:
        if lm[tip].y < lm[tip - 2].y:
            return False
    return True

def is_ok(lm):
    d = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y)
    return d < 0.04

# ---------------- LOOP ----------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect_for_video(mp_image, int(time.time() * 1000))

    if result.hand_landmarks:
        lm = result.hand_landmarks[0]
        index = lm[8]
        thumb = lm[4]

        x = int(index.x * WIDTH)
        y = int(index.y * HEIGHT)
        z = float(index.z)

        x, y = smooth(x, y)

        # -------- COLOR SELECT (THUMB HOVER) --------
        for i, col in enumerate(palette):
            px = 60 + i * 60
            py = 60
            if abs(int(thumb.x * WIDTH) - px) < 25 and abs(int(thumb.y * HEIGHT) - py) < 25:
                current_color = col

        # -------- ERASER --------
        if is_ok(lm):
            canvas[:] = 0
            strokes.clear()
            current_stroke = []
            continue

        # -------- STOP --------
        if is_fist(lm):
            if len(current_stroke) > 1:
                strokes.append(current_stroke)
            current_stroke = []
            smooth_points.clear()
        else:
            current_stroke.append([x, y, z, current_color])

    # -------- REDRAW --------
    canvas[:] = 0
    for stroke in strokes + [current_stroke]:
        for i in range(1, len(stroke)):
            x1, y1, _, c1 = stroke[i - 1]
            x2, y2, _, c2 = stroke[i]
            cv2.line(canvas, (x1, y1), (x2, y2), c1, 5)

    # -------- PALETTE UI --------
    for i, col in enumerate(palette):
        cv2.circle(frame, (60 + i * 60, 60), 20, col, -1)

    output = cv2.addWeighted(frame, 0.7, canvas, 1, 0)
    cv2.putText(output,
        "Index: Draw | Thumb: Color | OK: Erase | Fist: Stop",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("AirDraw 3D", output)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- SAVE ----------------
if len(current_stroke) > 1:
    strokes.append(current_stroke)

with open("strokes_3d.json", "w") as f:
    json.dump(strokes, f)
    cv2.imwrite("airdraw_2d.png", canvas)
print("🖼 2D drawing saved as airdraw_2d.png")


cap.release()
cv2.destroyAllWindows()
print("✅ Saved for 3D viewer")
