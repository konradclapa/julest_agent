from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

CONFIG_FILE = 'config.json'
TRANSLATIONS_FILE = 'translations.json'

def load_config():
    """Loads the entire configuration from config.json."""
    if not os.path.exists(CONFIG_FILE):
        return {'theme': 'dark', 'language': 'en'}
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {'theme': 'dark', 'language': 'en'}

def save_config(config):
    """Saves the entire configuration to config.json."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except IOError:
        print(f"Error: Could not write to {CONFIG_FILE}")

def load_translations():
    """Loads translations from translations.json"""
    try:
        with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        # Fallback to a minimal dictionary if translations are missing
        return {
            "en": {"message": "Translations file not found."},
            "el": {"message": "Το αρχείο μεταφράσεων δεν βρέθηκε."}
        }

# Load initial config and translations
config = load_config()
app.config['CURRENT_THEME'] = config.get('theme', 'dark')
app.config['CURRENT_LANGUAGE'] = config.get('language', 'en')
translations = load_translations()

@app.route('/', methods=['GET', 'POST'])
def index():
    current_language = app.config.get('CURRENT_LANGUAGE', 'en')
    lang_translations = translations.get(current_language, translations['en'])

    message = lang_translations["please_click_button"]
    if request.method == 'POST':
        if 'button1' in request.form:
            message = lang_translations["button1_clicked"]
        elif 'button2' in request.form:
            message = lang_translations["button2_clicked"]

    current_theme = app.config.get('CURRENT_THEME', 'dark')
    return render_template('index.html', message=message, current_theme=current_theme, lang=current_language, t=lang_translations)

@app.route('/toggle-theme')
def toggle_theme():
    config = load_config()
    current_theme = config.get('theme', 'dark')
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    config['theme'] = new_theme
    save_config(config)
    app.config['CURRENT_THEME'] = new_theme
    return redirect(url_for('index'))

@app.route('/toggle-language')
def toggle_language():
    config = load_config()
    current_language = config.get('language', 'en')
    new_language = 'el' if current_language == 'en' else 'en'
    config['language'] = new_language
    save_config(config)
    app.config['CURRENT_LANGUAGE'] = new_language
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
