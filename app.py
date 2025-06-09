from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

CONFIG_FILE = 'config.json'

def load_theme():
    """Loads theme from config.json"""
    if not os.path.exists(CONFIG_FILE):
        return 'dark' # Default theme if file doesn't exist
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('theme', 'dark')
    except (IOError, json.JSONDecodeError):
        return 'dark' # Default in case of error

def save_theme(theme):
    """Saves theme to config.json"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'theme': theme}, f)
    except IOError:
        print(f"Error: Could not write to {CONFIG_FILE}")

# Load initial theme
app.config['CURRENT_THEME'] = load_theme()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = "Please click a button."
    if request.method == 'POST':
        if 'button1' in request.form:
            message = "Button 1 was clicked!"
        elif 'button2' in request.form:
            message = "Button 2 was clicked!"
        # No need for an else unknown button here if POST is only from these buttons

    current_theme = app.config.get('CURRENT_THEME', load_theme())
    return render_template('index.html', message=message, current_theme=current_theme)

@app.route('/toggle-theme')
def toggle_theme():
    current_theme = app.config.get('CURRENT_THEME', load_theme())
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    save_theme(new_theme)
    app.config['CURRENT_THEME'] = new_theme
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
