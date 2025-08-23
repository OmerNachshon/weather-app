"""
WSGI entry point for Azure App Service
"""
from app import create_app

# Create app instance for WSGI server
app = create_app()

if __name__ == "__main__":
    app.run()
