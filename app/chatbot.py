"""High-level chat utilities (separate from the ML model)."""

from .ml_model import predict_mood
import random


# Response templates for positive sentiments
POSITIVE_RESPONSES = [
    "That sounds wonderful! I'm happy to hear that. 😊",
    "I'm so glad you're feeling good! 🌟",
    "That's amazing! Keep up the positive energy! ✨",
    "It's great to see you in such a good mood! 💪",
    "You sound uplifted! Tell me more about what's making you happy.",
    "That's fantastic! Your positivity is inspiring! 🎉",
]

# Response templates for negative sentiments
NEGATIVE_RESPONSES = [
    "I hear you. It's okay to feel this way. I'm here to listen and support you. 💜",
    "I'm sorry you're going through this. Remember, you're not alone. Let's talk about it.",
    "Your feelings are valid. I'm here to help you through this difficult time.",
    "Thank you for sharing. It's important to express what you're feeling. What do you need right now?",
    "I understand this is hard. You're brave for opening up. How can I support you?",
    "It's okay to struggle sometimes. Let's work through this together. 💚",
]

# Supportive keywords and responses
KEYWORD_RESPONSES = {
    'help': "I'm here to help! Could you tell me more about what you need assistance with?",
    'sad': "I sense you're feeling down. Would you like to talk about what's making you sad?",
    'happy': "That's wonderful! Being happy is something to celebrate! ✨",
    'anxious': "Anxiety can be challenging. Let's take a deep breath together. What's worrying you?",
    'tired': "Fatigue can affect our mood. Have you been taking care of yourself? Rest is important.",
    'stress': "Stress can be overwhelming. Remember to take breaks and practice self-care.",
    'alone': "Feeling alone is tough, but know that you have support. What would help right now?",
    'grateful': "Gratitude is a beautiful thing! Focusing on good things can improve your mood. 💛",
    'love': "That's wonderful! Positive connections uplift us. Tell me more! 💗",
    'hope': "Hope is powerful! It's a great foundation for positive change. 🌈",
}


def get_reply(user_text: str) -> tuple[str, str]:
    """Return a tuple (reply_message, sentiment) for the given user text."""
    
    sentiment = predict_mood(user_text)
    user_text_lower = user_text.lower()
    
    # Check for keywords first
    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in user_text_lower:
            return response, sentiment
    
    # Otherwise use sentiment-based responses
    if sentiment == 'Positive':
        reply = random.choice(POSITIVE_RESPONSES)
    else:
        reply = random.choice(NEGATIVE_RESPONSES)
    
    # Add follow-up question
    follow_up = get_follow_up(user_text_lower, sentiment)
    if follow_up:
        reply += f" {follow_up}"
    
    return reply, sentiment


def get_follow_up(user_text_lower: str, sentiment: str) -> str:
    """Generate a contextual follow-up question based on sentiment."""
    
    if sentiment == 'Positive':
        follow_ups = [
            "What's been the highlight of your day?",
            "What's contributing to your good mood?",
            "Anything else you'd like to share?",
            "How long have you been feeling this way?",
        ]
    else:
        follow_ups = [
            "When did you start feeling this way?",
            "What would help you feel better right now?",
            "Have you talked to anyone about this?",
            "What do you think might help?",
            "Would it help to talk more about this?",
        ]
    
    return random.choice(follow_ups) if follow_ups else ""
