import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/reproductive_farms'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/docs'
    API_URL = '/api'
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']