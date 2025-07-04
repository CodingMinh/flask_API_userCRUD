""" handles errors """
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from flask import jsonify
from app import db

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return jsonify(payload), status_code

def bad_request(message):
    return error_response(400, message)

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error_response(e.code)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        db.session.rollback()
        return error_response(500, "An unexpected error occurred")