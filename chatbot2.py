import os
import sys
import subprocess
import speech_recognition as sr
import random
import json

# Transformer Model Import
try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
except ImportError:
    print("Please install transformers: pip install transformers")
    sys.exit(1)

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

def speak_macos(text):
    """
    Text-to-speech for macOS using system 'say' command.
    Provides more robust error handling and voice options.
    """
    try:
        subprocess.run(['say', '-v', 'Samantha', text], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['say', text], check=True)
        except Exception as e:
            print(f"TTS Error: {e}")
            print(f"[Would have spoken]: {text}")

def recognize_speech():
    """
    Recognize speech from microphone with improved error handling.
    """
    try:
        with sr.Microphone() as source:
            print("Listening for your command...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing speech...")
                speech_text = recognizer.recognize_google(audio)
                print(f"You said: {speech_text}")
                return speech_text
            except sr.WaitTimeoutError:
                print("Listening timed out. No speech detected.")
                return None
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return None
    except Exception as e:
        print(f"Microphone access error: {e}")
        return None

def load_intents():
    """
    Load intents from intents.json file.
    """
    try:
        with open('intents.json', 'r') as file:
            intents = json.load(file)
        return intents
    except Exception as e:
        print(f"Error loading intents: {e}")
        sys.exit(1)

def match_intent(text, intents):
    """
    Enhanced intent matching with fuzzy matching and topic suggestions.
    Uses case-insensitive partial matching and provides suggestions.
    """
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # First, try exact pattern matching
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in text_lower:
                return random.choice(intent['responses'])
    
    # If no match found, try more flexible pattern matching
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in text_lower or text_lower in pattern.lower():
                return random.choice(intent['responses'])
    
    # If still no match, provide topic suggestions
    available_topics = [
        intent['tag'] for intent in intents['intents'] 
        if 'tag' in intent and intent['tag']
    ]
    
    suggestions = "I didn't understand that. Would you like to talk about: " + \
                  ", ".join(available_topics) + "? " + \
                  "Try saying something related to these topics."
    
    return suggestions
def load_intents(default_intents=None):
    """
    Load intents from intents.json file with a fallback to default intents.
    """
    default_intents = default_intents or {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hi", "hello", "hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            },
            {
                "tag": "goodbye",
                "patterns": ["bye", "goodbye", "see you later"],
                "responses": ["Goodbye!", "See you soon!", "Take care!"]
            },
            {
                "tag": "help",
                "patterns": ["help", "what can you do", "assistance"],
                "responses": ["I can help you with various topics. Ask me about greetings, farewells, or general conversation."]
            }
        ]
    }
    
    try:
        with open('intents.json', 'r') as file:
            intents = json.load(file)
        return intents
    except Exception as e:
        print(f"Error loading intents: {e}. Using default intents.")
        return default_intents
    
def initialize_chatbot():
    """
    Initialize the language model with error handling and parallelism disabled.
    """
    try:
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        chatbot = pipeline('text-generation', 
                           model=model, 
                           tokenizer=tokenizer,
                           max_length=200,
                           num_return_sequences=1)
        return chatbot, tokenizer
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)

def generate_response(chatbot, tokenizer, text, conversation_history):
    """
    Generate a conversational response using the language model.
    """
    try:
        context = " ".join(conversation_history[-3:])
        full_prompt = f"{context} {text}"
        responses = chatbot(full_prompt)
        
        if responses and len(responses) > 0:
            response = responses[0]['generated_text']
            if full_prompt in response:
                response = response.replace(full_prompt, '').strip()
            return response
        
        return "I'm not sure how to respond to that."
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm having trouble understanding right now."

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
        response = match_intent(text, intents)
        
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
    """
    Main entry point with dependency checks.
    """
    check_dependencies()
    chat()

if __name__ == "__main__":
    main()
