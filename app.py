# app.py (Updated)
import requests
from flask import Flask, render_template, request
import logging

# Configure logging at the top of app.py
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_joke', methods=['POST'])
def get_joke():

    # Just to keep track of user usage, that's a logging/usage history of the web site
    logging.info("Form data received: %s", request.form)

    # 1. Capture the form data
    category_choice = request.form.get('category_choice', 'any')
    custom_categories = request.form.getlist('categories')  # e.g. ["Programming", "Dark"]
    language = request.form.get('language', 'en')
    blacklist = request.form.getlist('blacklist')  # e.g. ["nsfw", "racist"]

    # 2. Build the categories string
    if category_choice not in ('any', 'custom'):
        category_choice = 'any'

        # If "custom" is chosen but no categories checked, we can do something:
    if category_choice == 'custom' and len(custom_categories) == 0:
        # Option 1: revert to "Any"
        # category_choice = 'any'
        # Option 2: show an error page or redirect back
        return render_template(
            'joke.html',
            error="Please select at least one custom category.",
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    if category_choice == 'any':
        category_string = 'Any'
    else:
        category_string = ','.join(custom_categories)

    # 3. Build the query parameters
    # Example: blacklistFlags=nsfw,racist&lang=en
    blacklist_string = ','.join(blacklist) if blacklist else ''

    # 4. Construct the final API URL
    base_url = 'https://v2.jokeapi.dev/joke'
    endpoint = f"{base_url}/{category_string}"

    # We'll store query parameters in a dict that requests can transform into a query string
    params = {
        'lang': language
    }
    # Only set blacklistFlags if we actually have any
    if blacklist_string:
        params['blacklistFlags'] = blacklist_string

    # Optional: We could force it to return either single or twopart jokes:
    # params['type'] = 'single,twopart'

    # 5. Call the API
    try:
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()  # Raise an HTTPError if status code isn't 200
    except requests.RequestException as e:
        # Handle connection errors, timeouts, non-200 status codes
        error_message = f"We don't have jokes with the selected parameters yet. Please try again and prefer selecting jokes in 'English' :D"
        return render_template(
            'joke.html',
            error=error_message,
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    # 6. Parse the JSON response
    data = response.json()
    if data.get('error'):
        # API returned a JSON error, e.g., no jokes found
        error_reason = data.get('message', 'Unknown error from JokeAPI')
        return render_template(
            'joke.html',
            error=f"JokeAPI Error: {error_reason}",
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    joke_type = data.get('type')
    joke_text = None
    joke_setup = None
    joke_delivery = None

    if joke_type == 'single':
        joke_text = data.get('joke')
    elif joke_type == 'twopart':
        joke_setup = data.get('setup')
        joke_delivery = data.get('delivery')

    # 7. Pass data to a template to display the joke
    return render_template(
        'joke.html',
        error=None,
        category_choice=category_choice,
        custom_categories=custom_categories,
        language=language,
        blacklist=blacklist,
        joke_type=joke_type,
        joke_text=joke_text,
        joke_setup=joke_setup,
        joke_delivery=joke_delivery
    )



if __name__ == '__main__':
    app.run(debug=True, port=5001)
