from flask import Blueprint, request, jsonify, abort
from db import db

users_bp = Blueprint('users', __name__)

class User(db.Model):
    __tablename__ = 'users'
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name  = data.get('name')
    email = data.get('email')
    if not name or not email:
        abort(400, 'Missing "name" or "email"')
    if User.query.filter_by(email=email).first():
        abort(400, 'Email already exists')
    u = User(name=name, email=email)
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify(u.to_dict())

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    u.name  = data.get('name', u.name)
    u.email = data.get('email', u.email)
    db.session.commit()
    return jsonify(u.to_dict())

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return '', 204
