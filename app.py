import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

app.config['DEBUG'] = bool(os.environ.get('DEBUG'))
app.jinja_env.filters['static'] = lambda name: url_for('static', filename=name)

@app.route('/')
def index():
    return render_template('index.tmpl')

@app.route('/drop_test/')
def drop_test():
    return render_template('drop_test.tmpl')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
