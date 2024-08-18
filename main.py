from website import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get the port from the environment variable, default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    # Run the app on host 0.0.0.0 and the specified port
    app.run(host='0.0.0.0', port=port)