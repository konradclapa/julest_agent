import os
import json
import pytest
from app import app as flask_app, save_config, load_config

CONFIG_FILE = 'config.json'

@pytest.fixture(scope='module')
def app_instance():
    """Create and configure a new app instance for each test module."""
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app_instance):
    """A test client for the app."""
    return app_instance.test_client()

@pytest.fixture(autouse=True)
def manage_config_file():
    """Ensures config.json is in a known state before each test and cleaned up after."""
    original_config = load_config()

    # Set to default state for the test
    save_config({"theme": "dark", "language": "en"})
    flask_app.config['CURRENT_THEME'] = 'dark'
    flask_app.config['CURRENT_LANGUAGE'] = 'en'

    yield

    # Restore original config
    save_config(original_config)

def test_default_theme_and_language(client):
    """Test that the default theme is dark and language is English."""
    response = client.get('/')
    assert response.status_code == 200

    config = load_config()
    assert config['theme'] == 'dark'
    assert config['language'] == 'en'

    response_data = response.data.decode('utf-8')
    assert '<body class="dark">' in response_data
    assert '&#127774;' in response_data
    assert 'Light Mode' in response_data
    assert 'Translate Greek' in response_data

def test_theme_toggling(client):
    """Test toggling the theme from dark to light and back to dark."""
    # Toggle to Light Mode
    client.get('/toggle-theme')
    config_light = load_config()
    assert config_light['theme'] == 'light'

    response_light_page = client.get('/')
    response_data_light = response_light_page.data.decode('utf-8')
    assert '<body class="light">' in response_data_light
    assert '&#127771;' in response_data_light
    assert 'Dark Mode' in response_data_light

    # Toggle back to Dark Mode
    client.get('/toggle-theme')
    config_dark = load_config()
    assert config_dark['theme'] == 'dark'

    response_dark_page = client.get('/')
    response_data_dark = response_dark_page.data.decode('utf-8')
    assert '<body class="dark">' in response_data_dark
    assert '&#127774;' in response_data_dark
    assert 'Light Mode' in response_data_dark

def test_language_toggling(client):
    """Test toggling the language from English to Greek and back to English."""
    # Toggle to Greek
    client.get('/toggle-language')
    config_greek = load_config()
    assert config_greek['language'] == 'el'

    response_greek_page = client.get('/')
    response_data_greek = response_greek_page.data.decode('utf-8')
    assert 'Μετάφραση στα Αγγλικά' in response_data_greek # "Translate to English" in Greek
    assert '&#127774;' in response_data_greek
    assert 'Φωτεινή λειτουργία' in response_data_greek # "Light Mode" in Greek

    # Toggle back to English
    client.get('/toggle-language')
    config_english = load_config()
    assert config_english['language'] == 'en'

    response_english_page = client.get('/')
    response_data_english = response_english_page.data.decode('utf-8')
    assert 'Translate Greek' in response_data_english
    assert '&#127774;' in response_data_english
    assert 'Light Mode' in response_data_english
