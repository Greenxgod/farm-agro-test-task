from flask import jsonify
from werkzeug.exceptions import HTTPException

class AppError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or {}

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = {
            'message': error.message,
            'errors': error.errors
        }
        return jsonify(response), error.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        response = {
            'message': error.description,
            'errors': {}
        }
        return jsonify(response), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        app.logger.error(f'Unhandled error: {error}')
        response = {
            'message': 'Internal server error',
            'errors': {}
        }
        return jsonify(response), 500