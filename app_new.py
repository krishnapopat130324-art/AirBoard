# app_new.py - FIXED VERSION
import cv2
import mediapipe as mp
import pyautogui
import pyttsx3
import json
import numpy as np
import pickle
import math
import threading
import time
import os
import urllib.request
import webbrowser
from flask import Flask, send_file
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()

print("🚀 AirBoard Starting...")

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

if not os.path.exists('hand_landmarker.task'):
    print("📥 Downloading hand landmark model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, 'hand_landmarker.task')
    print("✅ Model downloaded!")

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

try:
    with open('gesture_model.pkl', 'rb') as f:
        gesture_model = pickle.load(f)
    print("✅ Gesture model loaded")
except:
    print("⚠️ No gesture model found! Run train_model.py first")
    gesture_model = None

KEYBOARD_KEYS = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M'],
    ['SPACE','BACK','ENTER']
]

KEY_POSITIONS = {}
for row_idx, row in enumerate(KEYBOARD_KEYS):
    for col_idx, key in enumerate(row):
        x = (col_idx + 0.5) / len(row)
        y = (row_idx + 0.5) / len(KEYBOARD_KEYS)
        KEY_POSITIONS[key.lower()] = (x, y)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ===== GLOBAL VARIABLES =====
typing_mode = False
current_text = ""
last_tap_time = 0
TAP_COOLDOWN = 0.3

def classify_gesture(landmarks):
    if gesture_model is None:
        return None
    features = []
    for landmark in landmarks:
        features.extend([landmark.x, landmark.y, landmark.z])
    try:
        return gesture_model.predict([features])[0]
    except:
        return None

def get_key_from_position(x, y):
    closest_key = None
    closest_dist = float('inf')
    for key, pos in KEY_POSITIONS.items():
        dist = math.sqrt((x - pos[0])**2 + (y - pos[1])**2)
        if dist < closest_dist:
            closest_dist = dist
            closest_key = key
    if closest_dist < 0.15:
        return closest_key
    return None

def is_tap(landmarks):
    if len(landmarks) < 9:
        return False
    index_tip = landmarks[8]
    thumb_tip = landmarks[4]
    dist = math.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)
    return dist < 0.05

def is_hand_open(landmarks):
    if len(landmarks) < 21:
        return False
    tips = [8, 12, 16, 20]
    bases = [6, 10, 14, 18]
    open_count = 0
    for tip, base in zip(tips, bases):
        if landmarks[tip].y < landmarks[base].y:
            open_count += 1
    return open_count >= 3

app = Flask(__name__, static_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/style.css')
def serve_css():
    return send_file('style.css', mimetype='text/css')

@app.route('/script.js')
def serve_js():
    return send_file('script.js', mimetype='application/javascript')

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected via Socket.IO!')
    emit('connected', {'status': 'Connected'})
    threading.Thread(target=start_camera, daemon=True).start()

def start_camera():
    global typing_mode, current_text, last_tap_time
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera!")
        socketio.emit('error', {'message': 'Camera not found'})
        return
    
    print("✅✅✅ CAMERA IS OPEN! Look for the camera window!")
    print("👀 A window called 'AirBoard - Camera View' should appear!")
    print("✋ Show TWO open palms to start typing!")
    
    try:
        while True:
            success, img = cap.read()
            if not success:
                continue
            
            img = cv2.flip(img, 1)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
            
            detection_result = detector.detect(mp_image)
            
            if detection_result and detection_result.hand_landmarks:
                landmarks_list = detection_result.hand_landmarks
                
                h, w, _ = img.shape
                for hand_landmarks in landmarks_list:
                    for landmark in hand_landmarks:
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
                
                landmarks = landmarks_list[0]
                two_hands = len(landmarks_list) >= 2
                hand_open = is_hand_open(landmarks)
                gesture = classify_gesture(landmarks)
                
                # Show number of hands
                cv2.putText(img, f"Hands: {len(landmarks_list)}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # ---- GESTURE COMMANDS ----
                if gesture == 0 and two_hands:  # Two open palms = toggle typing
                    typing_mode = not typing_mode
                    socketio.emit('toggle_typing', {'mode': typing_mode, 'text': current_text})
                    speak("Typing mode " + ("on" if typing_mode else "off"))
                    print(f"⌨️ Typing mode: {'ON' if typing_mode else 'OFF'}")
                    # Small delay to prevent toggling too fast
                    time.sleep(0.5)
                
                elif gesture == 1:  # Fist = Backspace
                    if current_text:
                        current_text = current_text[:-1]
                        pyautogui.press('backspace')
                        socketio.emit('backspace', {'text': current_text})
                        speak("Backspace")
                        print(f"⌫ Backspace: {current_text}")
                    time.sleep(0.3)
                
                elif gesture == 2:  # Thumbs up = Enter
                    pyautogui.press('enter')
                    socketio.emit('enter', {'text': current_text})
                    speak("Enter")
                    print("↵ Enter pressed")
                    if typing_mode:
                        current_text = ""
                    time.sleep(0.3)
                
                elif gesture == 3:  # Peace sign = Read aloud
                    if current_text:
                        speak(current_text)
                        socketio.emit('speak', {'text': current_text})
                        print(f"🔊 Speaking: {current_text}")
                    time.sleep(0.3)
                
                # ---- TYPING MODE ----
                elif typing_mode and hand_open:
                    wrist = landmarks[0]
                    x, y = wrist.x, wrist.y
                    key = get_key_from_position(x, y)
                    tap_detected = is_tap(landmarks)
                    
                    if tap_detected and key:
                        current_time = time.time()
                        if current_time - last_tap_time > TAP_COOLDOWN:
                            last_tap_time = current_time
                            
                            if key == 'space':
                                current_text += ' '
                                pyautogui.press('space')
                            elif key == 'back':
                                if current_text:
                                    current_text = current_text[:-1]
                                    pyautogui.press('backspace')
                            elif key == 'enter':
                                pyautogui.press('enter')
                                current_text = ""
                            else:
                                current_text += key.upper()
                                pyautogui.write(key.upper())
                            
                            socketio.emit('type', {'key': key, 'text': current_text})
                            print(f"⌨️ Typed: {key} → '{current_text}'")
            
            # Display info on camera feed
            cv2.putText(img, f"Typing: {'ON' if typing_mode else 'OFF'}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                        (0, 255, 0) if typing_mode else (0, 0, 255), 2)
            cv2.putText(img, "Show 2 open palms to toggle typing", 
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.putText(img, f"Text: {current_text[-20:] if current_text else 'Waiting...'}", 
                        (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("AirBoard - Camera View", img)
            cv2.waitKey(1)
    
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("📸 Camera released")

if __name__ == "__main__":
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("🌐 Server running on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)