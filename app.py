import os
import base64
from flask import Flask, request, jsonify, render_template
from chatbot import enhanced_match_intent, generate_response, initialize_chatbot, load_intents, speak_macos, recognize_speech
import speech_recognition as sr

# Initialize Flask app
app = Flask(__name__)

# Load intents
intents = load_intents()

# Initialize chatbot
chatbot, tokenizer = initialize_chatbot()

conversation_history = []

@app.route("/")
def home():
    """
    Serve the main chat interface.
    """
    return render_template("index.html")

def text_to_speech(text):
    """
    Convert text to speech and return base64 encoded audio
    """
    try:
        # Use the existing speak_macos function to generate speech
        audio_path = "/tmp/response_audio.wav"
        speak_macos(text, output_file=audio_path)
        
        # Read the audio file and encode it
        with open(audio_path, 'rb') as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Remove the temporary file
        os.remove(audio_path)
        
        return audio_base64
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

def audio_to_text(audio_data):
    """
    Convert base64 encoded audio to text using speech recognition
    """
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data)
        
        # Save to a temporary file
        with open("/tmp/input_audio.wav", "wb") as f:
            f.write(audio_bytes)
        
        # Use speech recognition to convert audio to text
        r = sr.Recognizer()
        with sr.AudioFile("/tmp/input_audio.wav") as source:
            audio = r.record(source)
        
        # Recognize the speech
        text = r.recognize_google(audio)
        
        # Remove the temporary file
        os.remove("/tmp/input_audio.wav")
        
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Error in speech-to-text: {e}")
        return None

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chat messages from both text and audio input
    """
    global conversation_history
    
    # Get input type and data
    input_type = request.json.get("input_type", "text")
    input_data = request.json.get("message", "").strip()
    
    # Process audio input if applicable
    if input_type == "audio":
        user_message = audio_to_text(input_data)
        if not user_message:
            return jsonify({
                "response": "Sorry, I couldn't understand the audio.",
                "audio_response": None
            })
    else:
        # Text input
        user_message = input_data
    
    if not user_message:
        return jsonify({
            "response": "I didn't get that. Please try again.",
            "audio_response": None
        })

    # Check for a matched intent
    response = enhanced_match_intent(user_message, intents)

    # If no intent matched, use the transformer model
    if not response:
        conversation_history.append(user_message)
        response = generate_response(chatbot, tokenizer, user_message, conversation_history)
        conversation_history.append(response)

    # Convert response to audio
    audio_response = text_to_speech(response)

    return jsonify({
        "response": response,
        "audio_response": audio_response
    })

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    """
    Dedicated route for speech-to-text conversion
    """
    try:
        audio_data = request.json.get("audio", "").strip()
        if not audio_data:
            return jsonify({"text": "No audio data received"})
        
        text = audio_to_text(audio_data)
        
        if text:
            return jsonify({"text": text})
        else:
            return jsonify({"text": "Could not convert speech to text"})
    
    except Exception as e:
        return jsonify({"text": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)