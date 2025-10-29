# Button Clicker Application

This is a simple Flask web application that displays a page with two buttons and a message. It also features a theme toggling functionality (light/dark mode) with persistence.

## Project Structure

```
.
├── app.py              # Main Flask application file
├── config.json         # Stores the current theme setting
├── static
│   └── gemini.png      # Image asset for the Gemini logo
├── templates
│   └── index.html      # HTML template for the main page
└── test_app.py         # Pytest test suite for the application
```

-   **`app.py`**: The core of the application. It defines the Flask routes, handles button clicks, and manages theme switching.
-   **`config.json`**: A simple JSON file that stores the currently selected theme (`dark` or `light`). This allows the theme to persist across sessions.
-   **`static/`**: This directory contains static assets like images, CSS, and JavaScript files.
    -   **`gemini.png`**: The Gemini logo displayed on the page.
-   **`templates/`**: This directory contains the HTML templates used by Flask.
    -   **`index.html`**: The main and only page of the application. It includes the HTML structure, CSS for styling, and Jinja2 templating for dynamic content.
-   **`test_app.py`**: Contains the automated tests for the application, written using the pytest framework.

## Getting Started

### Prerequisites

-   Python 3.x
-   `pip` (Python package installer)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Install the required Python packages:
    ```bash
    pip install Flask pytest
    ```

### Running the Application

To run the application, execute the following command from the root of the project directory:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

### Running the Tests

To run the automated tests, use the following command from the root of the project directory:

```bash
pytest
```

This will discover and run the tests in `test_app.py`.
