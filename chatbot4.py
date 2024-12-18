import os
import sys
import subprocess
import speech_recognition as sr
import random
import json
import threading
import time
import os
import sys
import subprocess
import speech_recognition as sr
import random
import json

from chatbot3 import enhanced_match_intent, generate_response, initialize_chatbot, recognize_speech, speak_macos
# Transformer Model Import
try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
except ImportError:
    print("Please install transformers: pip install transformers")
    sys.exit(1)

# Global variables for thread-safe intent management
INTENTS_LOCK = threading.Lock()
GLOBAL_INTENTS = None

def load_intents(default_intents=None):
    """
    Thread-safe function to load intents from intents.json file.
    """
    global GLOBAL_INTENTS
    default_intents = default_intents or {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hi", "hello", "hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            },
            # ... other default intents ...
        ]
    }
    
    try:
        with INTENTS_LOCK:
            with open('intents.json', 'r') as file:
                intents = json.load(file)
                GLOBAL_INTENTS = intents
                return intents
    except Exception as e:
        print(f"Error loading intents: {e}. Using default intents.")
        with INTENTS_LOCK:
            GLOBAL_INTENTS = default_intents
        return default_intents

def watch_intents_file():
    """
    Background thread to monitor intents.json for changes.
    """
    global GLOBAL_INTENTS
    last_modified = 0
    
    while True:
        try:
            current_modified = os.path.getmtime('intents.json')
            if current_modified != last_modified:
                with INTENTS_LOCK:
                    with open('intents.json', 'r') as file:
                        GLOBAL_INTENTS = json.load(file)
                    print("Intents file updated successfully!")
                last_modified = current_modified
        except Exception as e:
            print(f"Error watching intents file: {e}")
        
        time.sleep(1)  # Check every second

def update_intents(text, response):
    """
    Enhanced update_intents with real-time file modification.
    """
    global GLOBAL_INTENTS
    try:
        # Load current intents with lock
        with INTENTS_LOCK:
            intents = GLOBAL_INTENTS.copy() if GLOBAL_INTENTS else load_intents()
        
        # Determine the most appropriate tag
        tag = "unknown_intent"
        keywords = {
            "help": ["help", "assist", "support", "problem"],
            "greeting": ["hi", "hello", "hey", "greetings"],
            "goodbye": ["bye", "goodbye", "farewell"],
            "question": ["what", "how", "why", "when", "where"]
        }
        
        for suggested_tag, tag_keywords in keywords.items():
            if any(keyword in text.lower() for keyword in tag_keywords):
                tag = suggested_tag
                break
        
        # Check if this tag already exists in intents
        tag_exists = False
        for intent in intents['intents']:
            if intent['tag'] == tag:
                # Add the new pattern if it doesn't already exist
                if text not in intent['patterns']:
                    intent['patterns'].append(text)
                # Add the new response if it doesn't already exist
                if response not in intent['responses']:
                    intent['responses'].append(response)
                tag_exists = True
                break
        
        # If tag doesn't exist, create a new intent
        if not tag_exists:
            new_intent = {
                "tag": tag,
                "patterns": [text],
                "responses": [response]
            }
            intents['intents'].append(new_intent)
        
        # Save the updated intents with lock
        with INTENTS_LOCK:
            with open('intents.json', 'w') as file:
                json.dump(intents, file, indent=4)
            GLOBAL_INTENTS = intents
        
        return True
    except Exception as e:
        print(f"Error updating intents: {e}")
        return False
def chat():
    """
    Main chat loop with voice interaction.
    """
    # Load intents from the file
    intents = load_intents()
    
    # Initialize chatbot
    chatbot, tokenizer = initialize_chatbot()
    
    print("Hello, I am JTalk. I am an AI voice assistant that can listen to both text and audio. I can also change your voice commands into text. This is JTalk version 1.0.0, released on December 18, 2024. How can I help you today?")
    speak_macos("Hello, I am JTalk. I am an AI voice assistant that can listen to both text and audio. I can also change your voice commands into text. This is JTalk version 1.0.0, released on December 18, 2024. How can I help you today?")
    
    conversation_history = []
    
    while True:
        # Listen for speech input
        text = recognize_speech()
        
        if not text:
            continue
        
        # Check for exit commands
        if any(exit_word in text.lower() for exit_word in ['exit', 'bye', 'goodbye', 'quit']):
            print("Goodbye!")
            speak_macos("Goodbye!")
            break
        
        # Try to match the text with intents
        response = enhanced_match_intent(text, intents)
        
        if not response:
            # If no match found, use the transformer model for generating a response
            conversation_history.append(text)
            response = generate_response(chatbot, tokenizer, text, conversation_history)
        
        # Add response to conversation history
        conversation_history.append(response)
        
        # Print and speak the response
        print(f"Bot: {response}")
        speak_macos(response)

def check_dependencies():
    """
    Validate and install missing dependencies for macOS.
    """
    required_libs = ['SpeechRecognition', 'transformers', 'pyaudio', 'torch']
    missing_libs = []
    for lib in required_libs:
        try:
            __import__(lib.lower().replace('-', '_'))
        except ImportError:
            missing_libs.append(lib)
    
    if missing_libs:
        print("Missing libraries detected. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_libs)
        except Exception as e:
            print(f"Error installing libraries: {e}")
            sys.exit(1)
    
def main():
    # Start the intents file watcher in a background thread
    intents_watcher = threading.Thread(target=watch_intents_file, daemon=True)
    intents_watcher.start()
    chat()

if __name__ == "__main__":
    main()