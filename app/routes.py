from flask import request, jsonify, render_template
from . import db
from .models import User, MoodLog
from .utils import hash_password, verify_password, append_to_csv
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .ml_model import predict_mood, train


# the blueprint is registered in __init__.py
from flask import Blueprint
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'msg': 'Username and password required'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'msg': 'User already exists'}), 400
        user = User(username=username, password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'User created'}), 201
    # GET -> show simple form for manual testing
    return render_template('login.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not verify_password(user.password_hash, password):
            return jsonify({'msg': 'Bad username or password'}), 401
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return render_template('login.html')


@bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    text = data.get('message')
    if not text:
        return jsonify({'msg': 'Message required'}), 400
    # determine sentiment and get a packaged reply
    from .chatbot import get_reply
    reply, sentiment = get_reply(text)
    # store to database
    user_id = get_jwt_identity()
    log = MoodLog(user_id=user_id, message=text, sentiment=sentiment)
    db.session.add(log)
    db.session.commit()
    # also append to CSV for later analysis/training
    append_to_csv('data/mood_dataset.csv', [text, sentiment], header=['text', 'sentiment'])
    return jsonify({'sentiment': sentiment, 'reply': reply})


@bp.route('/add_training', methods=['POST'])
@jwt_required()
def add_training():
    data = request.get_json()
    text = data.get('text')
    sentiment = data.get('sentiment')
    if sentiment not in ['Positive', 'Negative']:
        return jsonify({'msg': 'Sentiment must be Positive or Negative'}), 400
    # encode sentiment as 1/0
    val = 1 if sentiment == 'Positive' else 0
    append_to_csv('data/training_data.csv', [text, val], header=['text', 'sentiment'])
    # retrain model immediately
    train()
    return jsonify({'msg': 'Added training example and retrained'})


@bp.route('/dashboard')
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    logs = MoodLog.query.filter_by(user_id=user_id).order_by(MoodLog.timestamp.desc()).all()
    return render_template('dashboard.html', logs=logs)
