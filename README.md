# ✋ AirBoard - Type in the Air with AI

### Revolutionary Touchless Typing System Powered by Computer Vision & Artificial Intelligence

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square\&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green?style=flat-square\&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-AI-orange?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey?style=flat-square)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🚀 Overview

AirBoard is an innovative AI-powered touchless typing system that transforms hand gestures into text, commands, and voice interactions using only a webcam.

By combining Computer Vision, Machine Learning, and Real-Time Gesture Recognition, AirBoard enables users to interact with computers naturally without requiring a keyboard, mouse, or any specialized hardware.

The system tracks hand movements in real time, recognizes gestures using MediaPipe and a Random Forest classifier, and instantly converts them into meaningful actions.

### 💡 Key Idea

Imagine typing emails, controlling presentations, entering commands, or interacting with applications simply by moving your hands in the air.

AirBoard makes this possible.

---

## 🎯 Problem Statement

Traditional Human-Computer Interaction relies heavily on physical devices such as keyboards, mice, and touchscreens.

These interfaces can be limiting in scenarios involving:

* Accessibility challenges
* Sterile medical environments
* Touchless public systems
* Smart classrooms
* Virtual and augmented reality
* Gesture-based computing

AirBoard addresses these challenges by introducing a completely contact-free interaction experience.

---

## ✨ Features

### 🖐️ Air Typing

Type text without touching a keyboard.

### 🤖 AI-Powered Gesture Recognition

Uses MediaPipe Hand Tracking and Machine Learning to recognize gestures with high accuracy.

### 🎤 Voice Feedback

Every typed character and command can be spoken aloud instantly.

### ⚡ Real-Time Processing

Low-latency gesture detection and action execution.

### 👆 Smart Gesture Commands

Perform common actions using simple hand gestures.

### 🎨 Modern User Interface

Clean and responsive web interface with real-time visual feedback.

### 🔒 Privacy First

All processing occurs locally on the device.

### 🌍 Cross Platform

Supports Windows, Linux, and macOS.

---

## 🧠 How It Works

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   📸 Webcam                                                  │
│        ↓                                                    │
│   🖐️ Hand Detection (MediaPipe)                             │
│        ↓                                                    │
│   📍 Landmark Extraction (21 Hand Points)                   │
│        ↓                                                    │
│   🧠 Random Forest Gesture Classification                   │
│        ↓                                                    │
│   ⌨️ Text / Commands / Voice Feedback                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Workflow

1. Webcam captures live video frames.
2. MediaPipe detects hand landmarks.
3. Feature vectors are extracted.
4. Random Forest model classifies gestures.
5. System executes corresponding actions.
6. UI updates in real time.

---

## 🎮 Gesture Guide

| Gesture              | Action                  |
| -------------------- | ----------------------- |
| ✋✋ Two Open Palms    | Toggle Typing Mode      |
| 👌 Thumb + Index Tap | Select / Type Character |
| 👍 Thumbs Up         | Enter Key               |
| ✌️ Peace Sign        | Read Text Aloud         |
| 👊 Fist              | Backspace               |

---

## 🎯 Example Usage

### Typing "HELLO"

```text
✋✋  → Activate Typing Mode

Move hand to H → Tap → H
Move hand to E → Tap → E
Move hand to L → Tap → L
Move hand to L → Tap → L
Move hand to O → Tap → O

👍 → Enter
```

Result:

```text
HELLO
```

---

## 🛠 Technology Stack

| Technology    | Purpose                 |
| ------------- | ----------------------- |
| Python        | Core Development        |
| OpenCV        | Video Processing        |
| MediaPipe     | Hand Tracking           |
| Scikit-Learn  | Machine Learning        |
| Random Forest | Gesture Classification  |
| Flask         | Backend Server          |
| Socket.IO     | Real-Time Communication |
| PyAutoGUI     | Keyboard Simulation     |
| pyttsx3       | Offline Text-to-Speech  |
| HTML5         | Frontend Structure      |
| CSS3          | Styling                 |
| JavaScript    | Interactive UI          |

---

## 📊 Machine Learning Pipeline

### Data Collection

Gesture samples are captured using the webcam.

### Landmark Detection

MediaPipe extracts 21 hand landmarks.

### Feature Engineering

Coordinates are normalized and converted into feature vectors.

### Model Training

Random Forest Classifier learns gesture patterns.

### Prediction

Live gesture data is classified in real time.

### Action Mapping

Predicted gesture triggers the corresponding system action.

---

## 📂 Project Structure

```text
AirBoard/
│
├── app_new.py
├── train_model.py
├── run.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── models/
│   └── gesture_model.pkl
│
├── assets/
│   └── hand_landmarker.task
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/krishnapopat130324-art/AirBoard.git

cd AirBoard
```

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Train Gesture Model

Run the training script:

```bash
python train_model.py
```

Capture gesture samples when prompted.

Supported Gestures:

* Open Palm
* Fist
* Thumbs Up
* Peace Sign

The trained model will be saved automatically.

---

## ▶️ Run Application

```bash
python run.py
```

The application will:

* Start webcam tracking
* Launch Flask server
* Open browser automatically
* Begin real-time gesture recognition

Default URL:

```text
http://localhost:5000
```

---

## 📈 Performance

| Metric           | Value                   |
| ---------------- | ----------------------- |
| Gesture Accuracy | 91%+                    |
| Processing Speed | Real-Time               |
| Hand Landmarks   | 21 Points               |
| Supported Hands  | 2 Hands                 |
| Voice Feedback   | Offline                 |
| Platform Support | Windows / Linux / macOS |

---

## 🔧 Troubleshooting

### Camera Not Detected

```bash
python -c "import cv2; cap=cv2.VideoCapture(0); print(cap.isOpened())"
```

### Gesture Recognition Poor

* Improve lighting conditions
* Retrain the model
* Keep hand visible within frame

### Voice Feedback Not Working

```bash
pip install pyttsx3
```

Restart the application.

### WebSocket Connection Error

Ensure ports:

```text
5000
8765
```

are available.

---

## 🎯 Applications

### Healthcare

Touchless interaction in sterile environments.

### Accessibility

Assist users with mobility impairments.

### Smart Education

Interactive classrooms and presentations.

### Gaming

Gesture-controlled gaming experiences.

### Virtual Reality

Natural interaction within immersive environments.

### Public Systems

Contact-free kiosks and terminals.

---

## 👨‍💻 Author

### Krishna Popat

---

## ⭐ Support

If you found this project useful:

* Star the repository
* Share it with others
* Contribute improvements
* Provide feedback

---

## 🌟 Project Tagline

### "Type Anywhere. Touch Nothing."

### Building the Future of Human-Computer Interaction Through AI and Computer Vision.

Made with ❤️ using Python, OpenCV, MediaPipe, and Machine Learning.
