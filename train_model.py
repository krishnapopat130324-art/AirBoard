# train_model.py - FINAL VERSION for MediaPipe 1.0.0
import cv2
import mediapipe as mp
import numpy as np
import pickle
import time

print("🔄 Training Gesture Classifier...")
print("📸 Open your webcam and show each gesture when prompted")

# ========== NEW: MediaPipe 1.0.0 API ==========
# In 1.0.0, use mp.tasks.vision for hand landmarks

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Define gestures to collect
GESTURES = {
    0: "open_palm",
    1: "fist", 
    2: "thumbs_up",
    3: "peace_sign"
}

def collect_gesture_data(gesture_name, num_samples=20):
    """Collect hand landmark data for a specific gesture"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera! Please check your webcam.")
        return []
    
    samples = []
    
    print(f"\n✋ Show '{gesture_name}' gesture")
    print(f"📸 Press 'SPACE' to capture samples (need {num_samples})")
    print("⏹️ Press 'ESC' to skip this gesture")
    
    # Create hand landmarker
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                          num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)
    
    captured = 0
    while captured < num_samples:
        success, img = cap.read()
        if not success:
            continue
            
        # Flip for mirror effect
        img = cv2.flip(img, 1)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
        
        # Detect hand landmarks
        detection_result = detector.detect(mp_image)
        
        # Draw instructions on screen
        cv2.putText(img, f"Gesture: {gesture_name}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Samples: {captured}/{num_samples}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(img, "Press SPACE to capture, ESC to skip", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        if detection_result and detection_result.hand_landmarks:
            # Draw landmarks on image
            for hand_landmarks in detection_result.hand_landmarks:
                # Draw connections (simple visualization)
                for idx, landmark in enumerate(hand_landmarks):
                    h, w, _ = img.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(img, (x, y), 3, (0, 255, 255), -1)
                
                # Extract features (x, y, z for all landmarks)
                features = []
                for landmark in hand_landmarks:
                    features.extend([landmark.x, landmark.y, landmark.z])
                
                if len(features) > 0:
                    samples.append(features)
                    captured += 1
                    print(f"✅ Captured {captured}/{num_samples}")
        
        cv2.imshow("Collect Gestures", img)
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC to skip
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return samples

def main():
    X = []  # Features
    y = []  # Labels
    
    print("\n🎯 Collecting gesture data...")
    print("⚠️ Make sure your hand is clearly visible")
    print("💡 Good lighting helps a lot!")
    
    # Test camera first
    test_cap = cv2.VideoCapture(0)
    if not test_cap.isOpened():
        print("❌ ERROR: Could not open camera!")
        print("Please check your webcam connection and permissions.")
        return
    test_cap.release()
    
    # Download hand landmark model if not exists
    import urllib.request
    import os
    if not os.path.exists('hand_landmarker.task'):
        print("📥 Downloading hand landmark model...")
        url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        urllib.request.urlretrieve(url, 'hand_landmarker.task')
        print("✅ Model downloaded!")
    
    for label, gesture_name in GESTURES.items():
        samples = collect_gesture_data(gesture_name, num_samples=15)
        
        if len(samples) > 0:
            X.extend(samples)
            y.extend([label] * len(samples))
            print(f"✅ Collected {len(samples)} samples for '{gesture_name}'")
        else:
            print(f"⚠️ Skipped '{gesture_name}' (no samples collected)")
    
    if len(X) == 0:
        print("❌ No data collected! Please run again and show your hand.")
        return
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    print(f"\n📊 Total samples: {len(X)}")
    print("🧠 Training classifier...")
    
    # Train a Random Forest classifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Test accuracy
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Model accuracy: {accuracy:.2%}")
    
    # Save model
    with open('gesture_model.pkl', 'wb') as f:
        pickle.dump(clf, f)
    
    print("💾 Model saved as 'gesture_model.pkl'")
    print("🎉 Training complete! You can now run 'python run.py'")

if __name__ == "__main__":
    main()