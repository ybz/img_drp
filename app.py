import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = bool(os.environ.get('DEBUG'))

@app.route('/')
def index():
    return render_template('index.tmpl')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
