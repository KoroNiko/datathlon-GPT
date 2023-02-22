from app import app, server
from pages.homepage import homepage_callbacks

if __name__ == '__main__':
    # server.run(debug=True, port=8080)
    app.run_server(debug=True, port=8080)