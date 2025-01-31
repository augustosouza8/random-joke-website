# Random Joke Web Application

A Flask-based web application that generates random jokes using the JokeAPI. Users can customize their joke experience by selecting categories, languages, and content filters.

## Features

- Multiple joke categories (Programming, Misc, Dark, Pun, Spooky, Christmas)
- Support for multiple languages (Czech, German, English, Spanish, French, Portuguese)
- Content filtering options (NSFW, Religious, Political, Racist, Sexist, Explicit)
- Responsive web interface using Bootstrap
- Error handling and user feedback
- Debug information display

## Technologies Used

- Python 3.x
- Flask 3.1.0
- Bootstrap 5.3.0
- JokeAPI v2
- Requests library
- Gunicorn (for production deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/random-joke-web-app.git
cd random-joke-web-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

3. Use the web interface to:
   - Select joke categories (Any or Custom)
   - Choose your preferred language
   - Set content filters
   - Click "Show me the joke" to generate a random joke

## Project Structure

```
random-joke-web-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
└── templates/
    ├── base.html         # Base template with common elements
    ├── index.html        # Home page with joke configuration
    └── joke.html         # Joke display page
```

## API Integration

The application integrates with JokeAPI v2 (https://v2.jokeapi.dev/) to fetch jokes. The API endpoint is constructed based on user selections:

- Base URL: `https://v2.jokeapi.dev/joke`
- Parameters:
  - Category: Single or multiple categories
  - Language: User-selected language code
  - Blacklist flags: User-selected content filters

## Error Handling

The application includes comprehensive error handling for:
- API connection issues
- Invalid category selections
- Missing jokes for selected parameters
- General API errors

## Development

### Running in Debug Mode

```bash
flask run --debug --port=5001
```

### Adding New Features

1. Create a new branch for your feature
2. Implement the feature
3. Test thoroughly
4. Submit a pull request

## Production Deployment

The application is configured to run with Gunicorn in production:

```bash
gunicorn app:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Zuiliam
- Built with assistance from ChatGPT
- Deployed by Augusto
- Uses [JokeAPI](https://v2.jokeapi.dev/) for joke content
- Bootstrap for frontend styling