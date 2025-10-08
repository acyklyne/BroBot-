
import random
import datetime
import re
import time
import sys
import requests
from colorama import init, Fore, Style
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize
init(autoreset=True)

# Training data for Vector Space Model (TF-IDF + Cosine Similarity)
training_sentences = [
    "hello", "hi there", "hey", "good morning", "good afternoon",
    "how are you", "how do you do", "what's up", "how's it going",
    "what is your name", "who are you", "what are you called",
    "help me", "what can you do", "commands", "assist me",
    "tell me a joke", "make me laugh", "funny story", "joke please",
    "thank you", "thanks a lot", "appreciate it", "grateful",
    "what time is it", "current time", "tell me the time", "time now",
    "what's the weather", "how is the weather", "weather forecast", "weather today",
    "calculate 2+2", "what is 5*3", "compute something", "math problem",
    "bye", "goodbye", "see you later", "exit", "quit",
    "I have a problem", "issue with service", "complaint", "not satisfied",
    "order status", "track my order", "where is my purchase", "order update",
    "information", "details", "faq", "frequently asked questions"
]

labels = [
    "greet", "greet", "greet", "greet", "greet",
    "how_are", "how_are", "how_are", "how_are",
    "name", "name", "name",
    "help", "help", "help", "help",
    "joke", "joke", "joke", "joke",
    "thanks", "thanks", "thanks", "thanks",
    "time", "time", "time", "time",
    "weather", "weather", "weather", "weather",
    "calc", "calc", "calc", "calc",
    "bye", "bye", "bye", "bye", "bye",
    "complaint", "complaint", "complaint", "complaint",
    "order", "order", "order", "order",
    "inquiry", "inquiry", "inquiry", "inquiry"
]

# Vectorize training data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

# Loading animation
def loading_animation(duration=1.5):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(Fore.CYAN + f"\rBroBot is typing... {spinner[idx % len(spinner)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# Typing animation
def typing_animation(message, delay=0.02):
    for char in message:
        sys.stdout.write(Fore.CYAN + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

# Bot message
def bot(message):
    loading_animation()
    typing_animation("BroBot: " + message)

# Mock database / structured responses
mock_orders = {
    "1001": "Shipped. Expected delivery in 2 days.",
    "1002": "Processing. Estimated shipping tomorrow.",
    "1003": "Delivered. Thank you for your purchase!",
    "1004": "Cancelled. Refund processed."
}

faqs = [
    "Return policy: 30 days from delivery.", 
    "Shipping: Standard 3-5 days, Express 1-2 days.", 
    "Payment options: Credit card, PayPal, GCash.", 
    "Contact: support@company.com, +1234567890."
]

weather_options = ["sunny ☀️", "rainy 🌧️", "cloudy ☁️", "stormy ⛈️", "windy 🌬️"]

# Responses dictionary
responses = {
    "greet": ["Hello! Welcome to our customer service. How can I assist you today?", "Hi there! I'm here to help with your inquiries.", "Greetings! What can I do for you?"],
    "how_are": ["I'm doing well, thank you! How about you?", "I'm great! How can I help?", "All good here! What's on your mind?"],
    "name": ["I am BroBot, your friendly customer service chatbot 🤖", "You can call me BroBot!", "I'm BroBot, at your service."],
    "help": ["I can help with orders, complaints, FAQs, time, weather, calculations, and more. Just ask!", "Commands: greet, inquire, complain, order status, time, weather, calc, joke, bye.", "Let me know what you need help with."],
    "joke": ["Why did the computer show up at work late? It had a hard drive! 😄", "Why do programmers prefer dark mode? Because light attracts bugs! 🐛", "What do you call a computer that sings? A Dell! 🎤"],
    "thanks": ["You're welcome! Is there anything else?", "Happy to help! Have a great day.", "My pleasure. Feel free to ask more."],
    "time": ["The current time is {time}.", "It's {time} right now."],
    "weather": ["It's {weather} today!", "Weather: {weather}."],
    "calc": ["The result is {result}.", "Calculated: {result}."],
    "bye": ["Thank you for contacting us. Goodbye!", "Goodbye! Hope to see you again.", "Farewell! Take care."],
    "complaint": ["I'm sorry to hear that. Can you describe the issue?", "We apologize for the inconvenience. Let's resolve this.", "Thank you for feedback. How can we fix it?"],
    "order": ["Please provide your order number for status.", "I can track your order. What's the ID?", "For order updates, share the order number."],
    "inquiry": ["I'd be happy to help! What do you need?", "Sure, ask away!", "Information coming up. What specifically?"]
}

# Welcome
print(Fore.GREEN + "="*60)
print(Fore.GREEN + "👋 Welcome to BroBot Customer Service! Type 'bye' or 'exit' to quit.")
print(Fore.GREEN + "Ask about orders, complaints, FAQs, or chat freely.")
print(Fore.GREEN + "="*60 + "\n")

# Main loop
while True:
    user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()
    if not user_input:
        continue
    if user_input.lower() in ["bye", "exit", "quit"]:
        bot("Thank you for chatting! Goodbye! 👋")
        break

    # Order checking
    order_match = re.findall(r'\b\d{4,}\b', user_input)
    if order_match:
        order_id = order_match[0]
        if order_id in mock_orders:
            bot(f"Checking order {order_id}... Status: {mock_orders[order_id]} 🚚")
        else:
            bot(f"Order {order_id} not found. ❌")
        continue

    # FAQs
    faq_keywords = ["return", "shipping", "payment", "contact"]
    if any(word in user_input.lower() for word in faq_keywords):
        faq_found = [f for f in faqs if any(w.lower() in user_input.lower() for w in f.split())]
        if faq_found:
            bot(random.choice(faq_found))
            continue

    # Weather inquiries
    if "weather" in user_input.lower():
        bot(f"Today's weather is {random.choice(weather_options)}.")
        continue

    # Calculations
    calc_match = re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', user_input)
    if calc_match:
        expr = calc_match.group(1)
        try:
            result = eval(expr)
            bot(f"The result of {expr} is {result}.")
        except:
            bot("Sorry, I couldn't calculate that. ❌")
        continue

    # Vector Space Model: Compute similarity
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)[0]
    best_index = similarities.argmax()
    confidence = similarities[best_index]
    intent = labels[best_index]

    # Threshold for confidence
    if confidence < 0.1:  # Low confidence, fallback
        intent = "unknown"

    # Rule-based handling for dynamic responses
    if intent == "time":
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = random.choice(responses[intent]).format(time=now)
    elif intent == "weather":
        weather = random.choice(weather_options)
        response = random.choice(responses[intent]).format(weather=weather)
    elif intent == "calc":
        # Extract expression using regex
        expr_match = re.search(r'calc\s*(.+)', user_input) or re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', user_input)
        if expr_match:
            expr = expr_match.group(1).strip()
            try:
                result = eval(expr)
                response = random.choice(responses[intent]).format(result=result)
            except:
                response = "Sorry, I couldn't calculate that."
        else:
            response = "Please provide an expression like 'calc 2+2'."
    elif intent == "inquiry" and "faq" in user_input:
        response = random.choice(faqs)
    else:
        response = random.choice(responses.get(intent, ["I'm sorry, I didn't understand. Try 'help' for options."]))

    bot(response)

    if intent == "bye":
        break
