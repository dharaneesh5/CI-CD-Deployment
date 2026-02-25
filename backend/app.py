import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from routes import register_blueprints  # Import the helper function

app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')

# Load configuration
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SESSION_TYPE'] = Config.SESSION_TYPE
app.config['SESSION_PERMANENT'] = Config.SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = Config.SESSION_USE_SIGNER
app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE

# Enable CORS
CORS(app, supports_credentials=True)

# Register all blueprints
register_blueprints(app)

# Serve frontend pages
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_page(path):
    # Try serving as a file directly
    full_path = os.path.join(app.static_folder, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)
    
    # Try appending .html if it's not present
    if not path.endswith('.html'):
        html_path = path + '.html'
        if os.path.exists(os.path.join(app.static_folder, html_path)):
            return send_from_directory(app.static_folder, html_path)
            
    return not_found(None)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return send_from_directory(app.static_folder, 'index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return ('Internal server error', 500)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)