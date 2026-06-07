import cv2
import mediapipe as mp
import numpy as np
import math
import os


# ÇİÇEKLER

cicekler = []

for i in range(1, 11):
    path = f"assets/C{i}.png"

    if not os.path.exists(path):
        print(f"EKSİK DOSYA: {path}")
        exit()

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    cicekler.append(img)

current_step = 0


# MEDIAPIPE

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)


# WINDOW SETUP

cv2.namedWindow("KAMERA", cv2.WINDOW_NORMAL)
cv2.namedWindow("CICEK PANEL", cv2.WINDOW_NORMAL)


# LOOP

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    oran = 0


    # HAND TRACKING

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

            lms = hand_landmarks.landmark

            dist = math.hypot(
                lms[12].x - lms[0].x,
                lms[12].y - lms[0].y
            )

            oran = np.clip((dist - 0.1) / (0.3 - 0.1), 0, 1)

    # STEP CONTROL
    target = int(oran * 9)
    target = max(0, min(target, 9))

    if target > current_step:
        current_step += 1
    elif target < current_step:
        current_step -= 1

    # ÇİÇEK PANELİ
    flower = cicekler[current_step]

    panel = np.zeros((500, 500, 3), dtype=np.uint8)

    # büyük göster
    flower = cv2.resize(flower, (400, 400))

    fh, fw = flower.shape[:2]

    x = (500 - fw) // 2
    y = (500 - fh) // 2

    if flower.shape[2] == 4:
        alpha = flower[:, :, 3] / 255.0
    else:
        alpha = np.ones((fh, fw))

    for c in range(3):
        panel[y:y+fh, x:x+fw, c] = (
            (1 - alpha) * panel[y:y+fh, x:x+fw, c] +
            alpha * flower[:, :, c]
        )

    # TEXT PANEL
    cv2.putText(panel,
                f"CICEK SEVIYE: {current_step+1}/10",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2)

    cv2.putText(panel,
                f"ACILIK: {int(oran*100)}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (200, 200, 200),
                2)

    # SHOW WINDOWS
    cv2.imshow("KAMERA", frame)
    cv2.imshow("CICEK PANEL", panel)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()