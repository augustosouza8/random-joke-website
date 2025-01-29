# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """
    Home page route that renders a simple welcome page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # By default, Flask runs on port 5000, accessible at http://127.0.0.1:5000
    app.run(debug=True, port=5001)
