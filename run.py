# run.py - Start Everything with ONE Command
import os
import sys
import subprocess
import webbrowser
import time
import socket

print("""
╔═══════════════════════════════════════════╗
║          🚀 AIRBOARD LAUNCHER            ║
║         Type in the Air with AI          ║
╚═══════════════════════════════════════════╝
""")

def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except:
            return False

def install_dependencies():
    """Install required packages"""
    print("📦 Checking dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print("✅ Dependencies installed")
        return True
    except:
        print("⚠️ Could not install dependencies. Trying to continue...")
        return False

def check_model():
    """Check if gesture model exists"""
    if os.path.exists('gesture_model.pkl'):
        print("✅ Gesture model found")
        return True
    else:
        print("⚠️ No gesture model found!")
        print("📸 Running train_model.py to create one...")
        try:
            subprocess.call([sys.executable, "train_model.py"])
            return os.path.exists('gesture_model.pkl')
        except:
            print("❌ Could not train model. Please run 'python train_model.py' manually")
            return False

def start_app():
    """Start the main application"""
    print("\n🎯 Starting AirBoard...")
    print("📸 Opening camera...")
    print("🌐 Server will start at http://localhost:5000")
    print("🔌 WebSocket will start at ws://localhost:8765")
    print("\n⚠️ Make sure your webcam is connected and accessible")
    print("\n💡 GESTURE GUIDE:")
    print("   ✋ Open Palm (2 hands) = Toggle Typing Mode")
    print("   👍 Thumbs Up = Press Enter")
    print("   ✌️ Peace Sign = Read Text Aloud")
    print("   👊 Fist = Backspace")
    print("   👆 Index Tap = Type Letter")
    print("\n" + "="*50 + "\n")
    
    # Run main app - browser will open from inside app.py
    try:
        subprocess.call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")

def main():
    # Check ports
    if not check_port(5000):
        print("⚠️ Port 5000 is in use. Trying to continue...")
    if not check_port(8765):
        print("⚠️ Port 8765 is in use. Trying to continue...")
    
    # Install dependencies
    install_dependencies()
    
    # Check/create model
    check_model()
    
    # Start the app
    start_app()

if __name__ == "__main__":
    main()