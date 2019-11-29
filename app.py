from routes import admin
from flask import Flask
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'youwontguess'
basedir = os.path.abspath(os.path.dirname(__file__))
app.static_folder = 'static'
app.register_blueprint(admin)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
