from app import app, server

from pages.homepage import homepage_callbacks
from pages.homepage.homepage import homepage_layout

if __name__ == '__main__':
    app.layout = homepage_layout
    server.run(debug=True, port=8080)