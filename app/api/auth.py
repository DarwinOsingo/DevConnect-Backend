from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# NOTE: In production, use a secure and secret environment variable!
SECRET_KEY = 'devconnect-secret-key'

# Generate JWT Token
def generate_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=3)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# ===========================
# REGISTER
# ===========================
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        bio = data.get('bio', '')

        # Validation
        if not all([name, email, password, role]):
            return jsonify({"message": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists"}), 400

        # Create user
        user = User(name=name, email=email, role=role, bio=bio)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = generate_token(user)

        return jsonify({
            "user": user.to_dict(),
            "token": token
        }), 201

    except Exception as e:
        print("🚨 Registration error:", e)
        return jsonify({"message": "Server error during registration"}), 500

# ===========================
# LOGIN
# ===========================
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid credentials"}), 401

        token = generate_token(user)

        return jsonify({
            "user": user.to_dict(),
            "token": token
        }), 200

    except Exception as e:
        print("🚨 Login error:", e)
        return jsonify({"message": "Server error during login"}), 500

# ===========================
# VERIFY TOKEN
# ===========================
@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])

        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"user": user.to_dict()}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
