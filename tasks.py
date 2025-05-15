from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from db import db

tasks_bp = Blueprint('tasks', __name__)

class Task(db.Model):
    __tablename__ = 'tasks'
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(120), nullable=False)
    done       = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'created_at': self.created_at.isoformat()
        }

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at).all()
    return jsonify([t.to_dict() for t in tasks])

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        abort(400, 'Missing "title"')
    t = Task(title=title)
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    t = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    t.title = data.get('title', t.title)
    t.done  = data.get('done', t.done)
    db.session.commit()
    return jsonify(t.to_dict())

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return '', 204
