import os
import json
import pytest
from app import app as flask_app # Alias to avoid conflict with app fixture

CONFIG_FILE = 'config.json'
ORIGINAL_CONFIG_CONTENT = None

@pytest.fixture(scope='module')
def app_instance():
    """Create and configure a new app instance for each test module."""
    # Ensure flask_app.config is fresh for the test module
    flask_app.config['TESTING'] = True
    # Reload initial theme from config file for the test session
    # load_theme is a global function in app.py, not a method of flask_app
    from app import load_theme as app_load_theme # import specifically
    flask_app.config['CURRENT_THEME'] = app_load_theme()
    return flask_app

@pytest.fixture
def client(app_instance):
    """A test client for the app."""
    return app_instance.test_client()

@pytest.fixture(autouse=True)
def manage_config_file():
    """Ensures config.json is in a known state before each test and cleaned up after."""
    global ORIGINAL_CONFIG_CONTENT

    # Save current config if exists
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                ORIGINAL_CONFIG_CONTENT = json.load(f)
            except json.JSONDecodeError:
                ORIGINAL_CONFIG_CONTENT = None # Handle empty or invalid json
    else:
        ORIGINAL_CONFIG_CONTENT = None

    # Set to default dark theme for the test
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"theme": "dark"}, f)

    # Update app's theme setting from the file, as app startup would
    from app import load_theme as app_load_theme # import specifically
    flask_app.config['CURRENT_THEME'] = app_load_theme()


    yield # This is where the test runs

    # Restore original config or remove if it was created
    if ORIGINAL_CONFIG_CONTENT is not None:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(ORIGINAL_CONFIG_CONTENT, f)
    elif os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

    # Reset app's theme to what it was or default if necessary
    # This is important if tests run in sequence within the same app context in some runners
    if ORIGINAL_CONFIG_CONTENT and 'theme' in ORIGINAL_CONFIG_CONTENT:
         flask_app.config['CURRENT_THEME'] = ORIGINAL_CONFIG_CONTENT['theme']
    else:
         flask_app.config['CURRENT_THEME'] = 'dark' # Default if no original or no theme key


def test_default_theme(client):
    """Test that the default theme is dark."""
    # Ensure config is set to dark by fixture.
    # The manage_config_file fixture already sets the theme to dark and updates app config.
    from app import load_theme as app_load_theme # import specifically
    flask_app.config['CURRENT_THEME'] = app_load_theme() # ensure app syncs with file state

    response = client.get('/')
    assert response.status_code == 200

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    assert config['theme'] == 'dark'

    response_data = response.data.decode('utf-8')
    assert '<body class="dark">' in response_data
    assert '🌞 Light Mode' in response_data

def test_theme_toggling(client):
    """Test toggling the theme from dark to light and back to dark."""
    # Initial state should be dark (ensured by manage_config_file fixture)

    # 1. Toggle to Light Mode
    response_toggle_to_light = client.get('/toggle-theme')
    assert response_toggle_to_light.status_code == 302 # Redirect

    with open(CONFIG_FILE, 'r') as f:
        config_light = json.load(f)
    assert config_light['theme'] == 'light'
    assert flask_app.config['CURRENT_THEME'] == 'light'


    response_light_page = client.get('/')
    assert response_light_page.status_code == 200
    response_data_light = response_light_page.data.decode('utf-8')
    assert '<body class="light">' in response_data_light
    assert '🌜 Dark Mode' in response_data_light

    # 2. Toggle back to Dark Mode
    response_toggle_to_dark = client.get('/toggle-theme')
    assert response_toggle_to_dark.status_code == 302 # Redirect

    with open(CONFIG_FILE, 'r') as f:
        config_dark = json.load(f)
    assert config_dark['theme'] == 'dark'
    assert flask_app.config['CURRENT_THEME'] == 'dark'

    response_dark_page = client.get('/')
    assert response_dark_page.status_code == 200
    response_data_dark = response_dark_page.data.decode('utf-8')
    assert '<body class="dark">' in response_data_dark
    assert '🌞 Light Mode' in response_data_dark
