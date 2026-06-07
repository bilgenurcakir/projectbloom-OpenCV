import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math
import os


# STREAMLIT LAYOUT

st.set_page_config(layout="wide") #geniş modlu ekran
col1, col2 = st.columns(2) #iki sütuna böl
with col1:
    st.title("📷 Kamera")

with col2:
    st.title("🌸 Çiçek Paneli")

cam_placeholder = col1.empty()
flower_placeholder = col2.empty()
run = st.checkbox("Kamerayı Başlat") # kamera izniyle başlat


# MEDIAPIPE

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) # %70 eşik değeri için yakala


# ÇİÇEKLER

cicekler = []
for i in range(1, 11):
    path = f"assets/C{i}.png"
    if not os.path.exists(path):
        st.error(f"Eksik dosya: {path}")
        st.stop()

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.convertScaleAbs(img, alpha=1.15, beta=10) #parlaklığı arttır
    cicekler.append(img)

current_step = 0


# KAMERA

cap = cv2.VideoCapture(0)


# LOOP

while run:

    ret, frame = cap.read()
    if not ret:
        st.error("Kamera okunamadı")
        break

    frame = cv2.flip(frame, 1) #ayna efekti
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    oran = 0 # el açıklık oranı


    # HAND TRACKING

    if results.multi_hand_landmarks: #el algılanırsa
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks( #el iskeleti oluştur
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )
            lms = hand_landmarks.landmark  #21 adet gelecek

            dist = math.hypot(
                lms[12].x - lms[0].x, #0 bilek, 12 parmak ucu arasındaki uzaklık
                lms[12].y - lms[0].y
            )

            oran = np.clip((dist - 0.1) / (0.3 - 0.1), 0, 1)

    # -------------------------
    # STEP CONTROL
    # -------------------------
    target = int(oran * 9)
    target = max(0, min(target, 9))

    if target > current_step:
        current_step += 1
    elif target < current_step:
        current_step -= 1

    flower = cicekler[current_step]

    # -------------------------
    # BÜYÜK ÇİÇEK
    # -------------------------
    flower_w = int(w * 0.5)
    flower_h = int(h * 0.6)

    flower = cv2.resize(flower, (flower_w, flower_h))
    fh, fw = flower.shape[:2]

    x = (w - fw) // 2
    y = (h - fh) // 2

    # -------------------------
    # PANEL
    # -------------------------
    panel = np.zeros((h, w, 3), dtype=np.uint8)

    # -------------------------
    # 🌟 ALPHA FIX (EN ÖNEMLİ KISIM)
    # -------------------------
    alpha_strength = 0.9

    if flower.shape[2] == 4:
        alpha_map = flower[:, :, 3] / 255.0
    else:
        alpha_map = np.ones((fh, fw))

    # contrast + boost
    alpha_map = np.clip(alpha_map * 1.25, 0, 1) * alpha_strength

    # -------------------------
    # SAFE DRAW
    # -------------------------
    if y >= 0 and x >= 0 and y + fh < h and x + fw < w:

        for c in range(3):
            panel[y:y+fh, x:x+fw, c] = (
                (1 - alpha_map) * panel[y:y+fh, x:x+fw, c] +
                alpha_map * flower[:, :, c]
            )

    # -------------------------
    # MERGE
    # -------------------------
    combined = cv2.addWeighted(frame, 0.4, panel, 0.6, 0)

    # -------------------------
    # UI TEXT
    # -------------------------
    cv2.putText(combined,
                f"Seviye: {current_step+1}/10",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2)

    cv2.putText(combined,
                f"Acilik: {int(oran*100)}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (220, 220, 220),
                2)

    # -------------------------
    # STREAMLIT OUTPUT
    # -------------------------
    cam_placeholder.image(frame, channels="BGR")
    flower_placeholder.image(panel, channels="BGR")

cap.release()