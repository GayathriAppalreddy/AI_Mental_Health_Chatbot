import sys
sys.path.append(r'C:\Users\Cloud Analogy\Desktop\Projects\AI_Mental_Health_Chatbot')
from app import create_app
app = create_app()
print('DB', app.config['SQLALCHEMY_DATABASE_URI'])
from app.ml_model import predict_mood
print('prediction:', predict_mood('I am happy and joyful'))
