import random

VOCAB = {
    "names": ["Master", "Mister", "Sir", "Dad", "Mr. Kay", "Boss"],
    "greetings": ["Hey", "Hello", "Hi there", "Reporting for duty", "At your service"],
    "acknowledgments": ["I'm on it", "Give me one second", "Let me check that for you", "Looking into it right now"],
    "success": ["All done!", "Got it!", "Here's what I found:", "Take a look at this:"],
    "confusion": ["Hmm, I didn't quite catch that.", "I'm still learning, could you rephrase that?", "You lost me there."],
    "farewells": ["Goodbye!", "Catch you later!", "Going to sleep now.", "See you soon!"],
    "no_issues": ["Everything looks perfectly clean!", "Spotless!", "No problems found here!", "You're all good to go!"]
}

def speak(category):
    """Returns a random phrase from the chosen category"""
    return random.choice(VOCAB.get(category, [""]))
