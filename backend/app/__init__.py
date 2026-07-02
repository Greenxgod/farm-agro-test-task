from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
from app.extensions import db, migrate
from app.errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    
    # CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Swagger configuration
    swagger_config = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/docs'
    }
    
    swagger = Swagger(app, config=swagger_config)
    
    # Register blueprints
    from app.routes.farms import farms_bp
    from app.routes.reproduction_records import records_bp
    
    app.register_blueprint(farms_bp, url_prefix='/api/farms')
    app.register_blueprint(records_bp, url_prefix='/api/reproduction-records')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Reproductive Farms API',
            'docs': '/docs',
            'endpoints': {
                'farms': '/api/farms',
                'records': '/api/reproduction-records',
                'statistics': '/api/reproduction-records/statistics'
            }
        })
    
    return app