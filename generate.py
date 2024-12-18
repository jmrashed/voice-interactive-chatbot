import json
import random

# Base patterns from the original JSON
base_patterns = {
    "greetings": [
        "hi", "hey", "good evening", "good morning", "hello there", "what's up", 
        "howdy", "greetings", "nice to meet you", "long time no see"
    ],
    "salutations": [
        "see you later", "goodbye", "talk to you soon", "bye", "catch you later", 
        "farewell", "until next time", "take care", "see ya"
    ],
    "help": [
        "assist me", "I'm lost", "help", "can you help me?", "how does this work?", 
        "I need guidance", "what should I do?", "can you explain?", "I'm confused"
    ],
    "name": [
        "what's your name?", "what is your name?", "who are you?", "do you have a name?", 
        "what should I call you?", "introduce yourself", "what's your identity?"
    ],
    "weather": [
        "what's the weather like?", "will it snow tomorrow?", "is it raining today?", 
        "how's the weather?", "what's the forecast?", "any rain expected?", 
        "should I bring an umbrella?", "temperature today?"
    ],
    "location": [
        "what is my current location?", "where is this place?", "where am I?", 
        "can you find my location?", "help me with directions", "GPS location?"
    ],
    "product_inquiry": [
        "tell me about the features of this product", "can you tell me about this item?", 
        "what is this product?", "what features does this product have?", 
        "product details?", "tell me more about this", "specifications?"
    ],
    "pricing": [
        "is this expensive?", "what's the price?", "can you tell me the price?", 
        "how much does this cost?", "pricing information?", "cost details", 
        "is this affordable?"
    ],
    "order_status": [
        "where is my order?", "has my order shipped?", "what's the status of my order?", 
        "when will my order arrive?", "tracking my purchase", "order progress?"
    ],
    "support": [
        "I'm having trouble", "can you help me with a technical issue?", 
        "there's a problem with the service", "need technical support", 
        "something isn't working", "help with an error"
    ],
    "payment_inquiry": [
        "what payment methods are accepted?", "is there any discount?", 
        "how do I pay?", "can I pay via credit card?", "payment options?", 
        "any promotions?", "accepted payment methods?"
    ],
    "account_management": [
        "how do I create an account?", "how can I change my password?", 
        "how do I update my profile?", "account settings", "reset password", 
        "modify account details", "account management"
    ],
    "feedback": [
        "how can I provide feedback?", "I have some suggestions", 
        "I want to give feedback", "can I rate this service?", 
        "want to share my experience", "improvement suggestions"
    ],
    "maintenance": [
        "is this service available?", "why can't I access this?", 
        "is there a maintenance issue?", "is the site down?", 
        "service unavailable?", "experiencing access problems"
    ],
    "security": [
        "how do I protect my account?", "do you encrypt my information?", 
        "is this service safe?", "data protection?", "account security", 
        "how secure is my data?"
    ],
    "time": [
        "what's the current time?", "how late is it?", "can you tell me the time?", 
        "time check", "current time?", "what time is it now?"
    ],
    "product_return": [
        "what's your return policy?", "how do I return a product?", 
        "can I return an item?", "how can I exchange this?", 
        "return process?", "product return details"
    ]
}

# Corresponding response sets
base_responses = {
    "greetings": [
        "Hey there! What can I do for you?", "Hi! How can I help you?", 
        "Hello! How can I assist you today?", "Greetings! What brings you here?"
    ],
    "salutations": [
        "Farewell! Take care!", "See you later! Feel free to return anytime.", 
        "Goodbye! Have a great day!", "Until next time!"
    ],
    "help": [
        "I'm here to help! What can I assist you with?", 
        "Sure! What do you need help with?", 
        "I'm happy to assist! What are you struggling with?"
    ],
    "name": [
        "You can call me Activity Wizard!", 
        "My name is Activity Wizard, and I'm here to assist you.", 
        "I'm Activity Wizard, at your service."
    ],
    "weather": [
        "You can check weather services for live updates on the forecast.", 
        "I'm not sure, but you can check your local weather forecast!", 
        "I recommend using a weather app for up-to-date information."
    ],
    "location": [
        "You can check your current location using Google Maps or any similar app.", 
        "I don't have access to your location, but you can use GPS or a map app to find it."
    ],
    "product_inquiry": [
        "This product has many features! Would you like to know more details?", 
        "This product is designed for your convenience! Let me know if you need more info."
    ],
    "pricing": [
        "The pricing information is available on our website!", 
        "You can find the price by visiting our product page."
    ],
    "order_status": [
        "Please check your order status in your account.", 
        "I recommend you track your order via the tracking number provided."
    ],
    "support": [
        "I'll help you sort that out! Can you explain the issue?", 
        "I'm here to assist with technical issues. Please describe the problem."
    ],
    "payment_inquiry": [
        "You can pay using Visa, Mastercard, or PayPal.", 
        "We accept several payment methods including credit cards and PayPal."
    ],
    "account_management": [
        "You can create an account by visiting the registration page.", 
        "To update your profile, go to your account settings."
    ],
    "feedback": [
        "Your feedback is important to us. Please send us your suggestions.", 
        "We'd love to hear your feedback! Please share your thoughts."
    ],
    "maintenance": [
        "It looks like the site is undergoing maintenance. Please check back later.", 
        "We are currently working on updates. Thanks for your patience!"
    ],
    "security": [
        "We take your security seriously and encrypt your data to ensure safety.", 
        "Yes, your information is protected by encryption and other security measures."
    ],
    "time": [
        "You can check the time on your device.", 
        "Please check your phone or computer for the current time."
    ],
    "product_return": [
        "You can return the product by following our return policy on the website.", 
        "Please visit our returns section for detailed instructions."
    ]
}

# Generate intents with expanded patterns
def generate_intents():
    intents = []
    for tag, patterns in base_patterns.items():
        # Randomly select responses
        tag_responses = random.sample(base_responses[tag], min(3, len(base_responses[tag])))
        
        # Generate multiple variations for the tag
        num_variations = random.randint(50, 80)
        tag_patterns = random.choices(patterns, k=num_variations)
        
        intents.append({
            "tag": tag,
            "patterns": tag_patterns,
            "responses": tag_responses
        })
    
    return intents

# Final intent generation
final_intents = generate_intents()

# Save to JSON
with open("intents.json", "w") as f:
    json.dump({"intents": final_intents}, f, indent=4)

print(f"Generated intents.json with {len(final_intents)} tags and multiple patterns!")