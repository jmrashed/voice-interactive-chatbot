import csv
import random
import string

def generate_unique_tag():
    """Generate a unique tag by combining random words."""
    adjectives = ['smart', 'quick', 'clever', 'helpful', 'efficient', 'advanced', 'friendly', 'intelligent', 
                  'responsive', 'dynamic', 'adaptive', 'proactive', 'innovative', 'versatile', 'comprehensive']
    nouns = ['assistant', 'bot', 'helper', 'guide', 'advisor', 'companion', 'system', 'interface', 
             'wizard', 'agent', 'platform', 'service', 'solution', 'tool', 'engine']
    
    return f"{random.choice(adjectives)}_{random.choice(nouns)}_{random.randint(100, 999)}"

def generate_pattern():
    """Generate a unique conversational pattern."""
    templates = [
        "how do I {verb} {object}?",
        "can you help me with {object}?",
        "what's the best way to {verb} {object}?",
        "I need assistance regarding {object}",
        "tell me about {object}",
        "help me understand {object}",
        "can you explain {object} to me?",
        "I'm looking for information about {object}"
    ]
    
    verbs = ['manage', 'handle', 'use', 'understand', 'learn', 'explore', 'discover', 'implement']
    objects = ['this feature', 'my account', 'the process', 'the service', 'the product', 
               'the system', 'the solution', 'the application', 'my request']
    
    return random.choice(templates).format(verb=random.choice(verbs), object=random.choice(objects))

def generate_response():
    """Generate a helpful, context-aware response."""
    response_templates = [
        "Let me help you with {object}. {detail}",
        "Great question about {object}! {detail}",
        "Here's what you need to know about {object}: {detail}",
        "I'm glad you asked about {object}. {detail}",
        "Regarding {object}, here's some useful information: {detail}"
    ]
    
    objects = ['this feature', 'your request', 'the process', 'our service', 'the product', 
               'the system', 'the solution', 'the application']
    
    details = [
        "Our team is dedicated to providing the best support.",
        "We strive to make your experience as smooth as possible.",
        "Feel free to ask for more specific details if needed.",
        "Our goal is to ensure your complete satisfaction.",
        "We're committed to helping you succeed.",
        "Your feedback is valuable to us.",
        "We continuously improve our services based on user needs."
    ]
    
    return random.choice(response_templates).format(
        object=random.choice(objects), 
        detail=random.choice(details)
    )

# Generate 1000 unique intents
unique_tags = set()
intents = []

while len(intents) < 1000:
    tag = generate_unique_tag()
    if tag not in unique_tags:
        unique_tags.add(tag)
        
        # Generate multiple patterns and responses for each tag
        num_patterns = random.randint(3, 6)
        num_responses = random.randint(2, 4)
        
        patterns = [generate_pattern() for _ in range(num_patterns)]
        responses = [generate_response() for _ in range(num_responses)]
        
        intents.append({
            'tag': tag,
            'patterns': patterns,
            'responses': responses
        })

# Write to CSV
with open('intents.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tag', 'pattern', 'response']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    
    for intent in intents:
        for pattern in intent['patterns']:
            for response in intent['responses']:
                writer.writerow([intent['tag'], pattern, response])

print(f"Generated intents.csv with {len(intents)} unique tags and their patterns/responses!")