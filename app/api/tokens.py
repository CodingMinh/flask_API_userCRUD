""" handles token auth """
from app.api.auth import basic_auth, token_auth
from flask import jsonify
from app import db
from app.api import bp

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # the get_token() here is from User model in models.py
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    # revoke_token() here is also from User model
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204