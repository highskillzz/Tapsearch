from routes import admin
import os
from flask import Flask, render_template

app = Flask(__name__, static_folder="build/static", template_folder="build")
basedir = os.path.abspath(os.path.dirname(__file__))
app.register_blueprint(admin)

# Serve React App
@admin.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
