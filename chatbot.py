import os
import sys
import subprocess
import speech_recognition as sr
import random

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
        # Use a specific voice, adjust as needed
        # Some available voices: Alex, Samantha, Victoria, etc.
        subprocess.run(['say', '-v', 'Samantha', text], check=True)
    except subprocess.CalledProcessError:
        # Fallback to default voice if specified voice fails
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
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                # Listen with timeout
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing speech...")
                
                # Recognize using Google Speech Recognition
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

def initialize_chatbot():
    """
    Initialize the language model with error handling and parallelism disabled.
    """
    try:
        # Disable tokenizers parallelism
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        
        # Rest of your existing initialization code...
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
        # Prepare context by combining conversation history
        context = " ".join(conversation_history[-3:])  # Use last 3 turns for context
        
        # Combine context and current input
        full_prompt = f"{context} {text}"
        
        # Generate response
        responses = chatbot(full_prompt)
        
        # Debug print
        print(f"Raw responses: {responses}")
        
        # Extract the generated text
        if responses and len(responses) > 0:
            # More robust response extraction
            response = responses[0]['generated_text']
            if full_prompt in response:
                response = response.replace(full_prompt, '').strip()
            
            # Ensure non-empty response
            if not response:
                return random.choice([
                    "I'm not sure how to respond to that.",
                    "Could you tell me more?",
                    "That's interesting. Can you elaborate?"
                ])
            
            return response
        
        # Fallback responses
        return random.choice([
            "I'm not sure how to respond to that.",
            "Could you tell me more?",
            "That's interesting. Can you elaborate?",
            "I'm listening. Go on."
        ])
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm having trouble understanding right now."


def chat():
    """
    Main chat loop with voice interaction.
    """
    # Initialize chatbot
    chatbot, tokenizer = initialize_chatbot()
    
    print("Hello, I'm your voice assistant. How can I help you today?")
    speak_macos("Hello, I'm your voice assistant. How can I help you today?")
    
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
        
        try:
            # Generate response
            conversation_history.append(text)
            response = generate_response(chatbot, tokenizer, text, conversation_history)
            
            # Add response to conversation history
            conversation_history.append(response)
            
            # Print and speak the response
            print(f"Bot: {response}")
            speak_macos(response)
        
        except Exception as e:
            print(f"Error processing response: {e}")
            speak_macos("I'm having trouble processing that request.")

def check_dependencies():
    """
    Validate and install missing dependencies for macOS.
    """
    # Check for required Python libraries
    required_libs = [
        'SpeechRecognition', 
        'transformers', 
        'pyaudio',
        'torch'
    ]
    
    missing_libs = []
    for lib in required_libs:
        try:
            __import__(lib.lower().replace('-', '_'))
        except ImportError:
            missing_libs.append(lib)
    
    if missing_libs:
        print("Missing libraries detected. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_libs)
        except Exception as e:
            print(f"Error installing libraries: {e}")
            print("Please install manually:")
            for lib in missing_libs:
                print(f"pip install {lib}")
            sys.exit(1)

def main():
    """
    Main entry point with dependency checks.
    """
    # Check and install dependencies
    check_dependencies()
    
    # Start chat
    chat()

if __name__ == "__main__":
    main()