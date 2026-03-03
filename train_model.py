"""Standalone script to retrain the sentiment analysis model.
Delegates to the training logic in app.ml_model so that the same
behavior is shared with the running application.
"""

from app.ml_model import train

if __name__ == '__main__':
    train()
