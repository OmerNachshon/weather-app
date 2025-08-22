"""
Configuration settings for the Weather Forecast App
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Configuration
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    EXPOSE_API_KEY_IN_HTML = os.environ.get("EXPOSE_API_KEY_IN_HTML", "0") == "1"
    
    # Application Settings
    ITEMS_PER_PAGE = 10
    USER_FORECAST_LIMIT = 5
    WEATHER_API_TIMEOUT = 10
    
    @staticmethod
    def init_app(app):
        """Initialize app with this configuration"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        "sqlite:///weather_dev.db"
    )


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///weather.db"
    )
    
    @staticmethod
    def init_app(app):
        """Initialize production app"""
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    """Testing configuration"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
