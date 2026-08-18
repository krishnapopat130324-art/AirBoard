// script.js - Updated with better feedback
const socket = io();

const statusEl = document.getElementById('status');
const typingModeEl = document.getElementById('typing-mode');
const gestureDisplay = document.getElementById('gesture-display');
const textOutput = document.getElementById('text-output');
const connectionStatus = document.getElementById('connection-status');
const textDisplay = document.querySelector('.text-display');

socket.on('connect', function() {
    statusEl.textContent = 'Connected';
    statusEl.className = 'status-value status-on';
    connectionStatus.textContent = '🟢 Connected';
    connectionStatus.className = 'status-badge connected';
    console.log('✅ Connected to server!');
});

socket.on('disconnect', function() {
    statusEl.textContent = 'Disconnected';
    statusEl.className = 'status-value status-off';
    connectionStatus.textContent = '⚪ Disconnected';
    connectionStatus.className = 'status-badge disconnected';
    console.log('⚠️ Disconnected from server');
});

socket.on('toggle_typing', function(data) {
    updateTypingMode(data.mode);
    // Show gesture feedback
    gestureDisplay.textContent = data.mode ? '✋✋ Typing ON' : '✋✋ Typing OFF';
    setTimeout(() => {
        gestureDisplay.textContent = '✋ Ready';
    }, 1000);
});

socket.on('type', function(data) {
    highlightKey(data.key);
    updateText(data.text);
    gestureDisplay.textContent = `👌 Tapped: ${data.key.toUpperCase()}`;
    setTimeout(() => {
        gestureDisplay.textContent = '✋ Ready';
    }, 500);
});

socket.on('backspace', function(data) {
    updateText(data.text);
    highlightKey('back');
    gestureDisplay.textContent = '👊 Backspace';
    setTimeout(() => {
        gestureDisplay.textContent = '✋ Ready';
    }, 500);
});

socket.on('enter', function(data) {
    highlightKey('enter');
    gestureDisplay.textContent = '👍 Enter';
    setTimeout(() => {
        gestureDisplay.textContent = '✋ Ready';
    }, 500);
});

socket.on('speak', function(data) {
    gestureDisplay.textContent = '🔊 Speaking...';
    setTimeout(() => {
        gestureDisplay.textContent = '✋ Ready';
    }, 2000);
});

function updateTypingMode(mode) {
    if (mode) {
        typingModeEl.textContent = '🟢 ON';
        typingModeEl.className = 'status-value mode-on';
        textDisplay.classList.add('active');
    } else {
        typingModeEl.textContent = '⛔ OFF';
        typingModeEl.className = 'status-value mode-off';
        textDisplay.classList.remove('active');
    }
}

function updateText(text) {
    if (text && text.length > 0) {
        textOutput.textContent = text;
    } else {
        textOutput.textContent = 'Type in the air...';
    }
}

function highlightKey(key) {
    document.querySelectorAll('.key').forEach(k => k.classList.remove('active'));
    
    document.querySelectorAll('.key').forEach(k => {
        if (k.dataset.key === key) {
            k.classList.add('active');
            setTimeout(() => {
                k.classList.remove('active');
            }, 300);
        }
    });
}

console.log('🚀 AirBoard frontend loaded!');
console.log('📖 INSTRUCTIONS:');
console.log('  ✋✋ Two open palms = Toggle typing ON/OFF');
console.log('  👌 Tap (thumb+index) = Type selected key');
console.log('  👍 Thumbs up = Press ENTER');
console.log('  ✌️ Peace sign = Read text aloud');
console.log('  👊 Fist = Backspace');