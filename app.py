import os
from flask import Flask

app = Flask(__name__)
app.configi['DEBUG'] = bool(os.environ.get('DEBUG'))

@app.route('/')
def index():
    return 'Putzify is currently unavailable'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
