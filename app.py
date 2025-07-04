# activate venv: & "C:\Users\Hi Windows 11 23\Desktop\Python\flask_API_userCRUD\.venv\Scripts\Activate.ps1"

from flask import Flask, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import sqlalchemy as sa
from app.errors import bad_request, register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
register_error_handlers(app)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return jsonify(User.to_collection_dict(sa.select(User), page, per_page, 'get_users'))

# get a user with given id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(db.get_or_404(User, id).to_dict())

# create new users
@app.route('/users', methods=['POST'])
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
    return jsonify(user.to_dict()), 201, {'Location': url_for('get_user', id=user.id)}

# update/modify a user with given id
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'username' in data and user.username != data['username'] and db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return bad_request('please use a different username')

    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

# delete a given user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted'})

if __name__ == '__main__':
    app.run(debug=True)

from app.models import User
import app.auth as auth, app.errors as errors, app.tokens as tokens