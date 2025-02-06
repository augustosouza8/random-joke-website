import requests
from flask import Flask, render_template, request
import logging

# Configure logging for debugging and production usage analytics
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    """
    Home route that renders the main page with the joke configuration form.
    """
    return render_template('index.html')

@app.route('/get_joke', methods=['POST'])
def get_joke():
    """
    Endpoint to process the form submission, call JokeAPI based on user inputs,
    and render the joke display page.
    """
    # Log the incoming form data for usage tracking
    logging.info("Form data received: %s", request.form)

    # 1. Capture form data from the POST request
    category_choice = request.form.get('category_choice', 'any')
    custom_categories = request.form.getlist('categories')  # e.g. ["Programming", "Dark"]
    language = request.form.get('language', 'en')
    blacklist = request.form.getlist('blacklist')  # e.g. ["nsfw", "racist"]

    # Validate category_choice. If an unknown value is provided, default to 'any'
    if category_choice not in ('any', 'custom'):
        category_choice = 'any'

    # If "custom" is selected but no categories are checked, return an error
    if category_choice == 'custom' and not custom_categories:
        error_message = "Please select at least one custom category."
        return render_template(
            'joke.html',
            error=error_message,
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    # 2. Build the category string based on the selection
    if category_choice == 'any':
        category_string = 'Any'
    else:
        category_string = ','.join(custom_categories)

    # 3. Build query parameters for JokeAPI
    params = {'lang': language}
    if blacklist:
        params['blacklistFlags'] = ','.join(blacklist)

    # 4. Construct the API URL
    base_url = 'https://v2.jokeapi.dev/joke'
    endpoint = f"{base_url}/{category_string}"

    try:
        # Make the API request (with a timeout for production readiness)
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()  # Raise an error for non-200 responses
    except requests.RequestException as e:
        logging.error("Error fetching joke: %s", e)
        error_message = (
            "We don't have jokes with the selected parameters yet. "
            "Please try again and consider selecting 'English'."
        )
        return render_template(
            'joke.html',
            error=error_message,
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    # 5. Parse the JSON response from JokeAPI
    data = response.json()
    if data.get('error'):
        error_reason = data.get('message', 'Unknown error from JokeAPI')
        return render_template(
            'joke.html',
            error=f"JokeAPI Error: {error_reason}",
            category_choice=category_choice,
            custom_categories=custom_categories,
            language=language,
            blacklist=blacklist
        )

    # 6. Extract joke data depending on the joke type
    joke_type = data.get('type')
    joke_text = data.get('joke') if joke_type == 'single' else None
    joke_setup = data.get('setup') if joke_type == 'twopart' else None
    joke_delivery = data.get('delivery') if joke_type == 'twopart' else None

    # 7. Render the joke page with the data received from JokeAPI
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
    # Run the Flask development server on port 5001 with debug enabled
    app.run(debug=True, port=5001)
