
from flask import Blueprint, jsonify, request
from src.models.user import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Username and email are required'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | 
            (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User with this username or email already exists'
            }), 409
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
