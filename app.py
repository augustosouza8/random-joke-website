# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    """
    Home page route that renders index.html.
    """
    return render_template('index.html')

@app.route('/get_joke', methods=['POST'])
def get_joke():
    """
    This route receives form data:
    - category_choice: 'any' or 'custom'
    - categories: list of categories if 'custom' is chosen
    - language: selected language
    - blacklist: list of blacklisted content flags
    """
    category_choice = request.form.get('category_choice', 'any')
    # For checkboxes, we can get them as a list using getlist
    custom_categories = request.form.getlist('categories')  # returns a list, e.g., ['Programming', 'Dark']
    language = request.form.get('language', 'en')
    blacklist = request.form.getlist('blacklist')  # also a list

    # For now, let's just echo back the user’s selections on a basic results page
    # We'll create or reuse a simple template, say 'results.html'.
    return render_template(
        'results.html',
        category_choice=category_choice,
        custom_categories=custom_categories,
        language=language,
        blacklist=blacklist
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
