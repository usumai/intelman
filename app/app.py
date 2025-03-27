from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World from Intel-Manager!"

if __name__ == '__main__':
    # Run the app on all available interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
