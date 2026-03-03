import os

# Define the structure
base = "AI_Mental_Health_Chatbot"
folders = [
    "app/templates", "app/static/css", "app/static/js", "app/static/images",
    "data", "models"
]
files = [
    "app/__init__.py", "app/routes.py", "app/models.py", "app/chatbot.py", 
    "app/ml_model.py", "app/utils.py", "app/templates/index.html", 
    "app/templates/login.html", "app/templates/dashboard.html",
    "data/training_data.csv", "data/mood_dataset.csv",
    "models/sentiment_model.pkl", "models/vectorizer.pkl",
    "config.py", "run.py", "requirements.txt", "Dockerfile"
]

for folder in folders:
    os.makedirs(os.path.join(base, folder), exist_ok=True)

for file in files:
    with open(os.path.join(base, file), 'w') as f:
        pass # Creates empty files
print(f"Project structure for '{base}' has been created.")
