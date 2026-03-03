"""High-level chat utilities (separate from the ML model)."""

from .ml_model import predict_mood


def get_reply(user_text: str) -> tuple[str, str]:
    """Return a tuple (reply_message, sentiment) for the given user text."""
    sentiment = predict_mood(user_text)
    if sentiment == 'Positive':
        reply = "I'm glad you're feeling good. Tell me more!"
    else:
        reply = "I'm sorry you're feeling down. I'm here to listen."
    return reply, sentiment
