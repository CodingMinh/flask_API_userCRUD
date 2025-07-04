# activate venv: & "C:\Users\Hi Windows 11 23\Desktop\Python\flask_API_userCRUD\.venv\Scripts\Activate.ps1"

from flask import request, url_for, jsonify, abort
import sqlalchemy as sa
from app.api.errors import bad_request
from app.models import User
from app import db
from app.api import bp
from app.api.auth import token_auth

# get all users
@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return jsonify(User.to_collection_dict(sa.select(User), page, per_page, 'api.get_users'))

# get a user with given id
@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(db.get_or_404(User, id).to_dict())

# create new users
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password')
    if db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return bad_request('please use a different username')
    
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201, {'Location': url_for('api.get_user', id=user.id)}

# update/modify a user with given id
@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
        
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'username' in data and user.username != data['username'] and db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return bad_request('please use a different username')

    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

# delete a given user
@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted'})