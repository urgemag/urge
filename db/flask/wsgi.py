import logging
from setting import debug_mode
from main import app
if __name__ == "__main__":
    app.run(debug=debug_mode)