import os
from flask import Flask, render_template, url_for, request
from werkzeug import secure_filename
from tempfile import mkdtemp

UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER'] if 'UPLOAD_FOLDER' in os.environ else mkdtemp()

app = Flask(__name__)

app.config['DEBUG'] = bool(os.environ.get('DEBUG'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.filters['static'] = lambda name: url_for('static', filename=name)

@app.route('/')
def index():
    return render_template('index.tmpl')

@app.route('/drop_test/')
def drop_test():
    return render_template('drop_test.tmpl')

@app.route('/face_upload', methods=['POST'])
def upload_for_detect():
    if request.method == 'POST':
        print 'inside func'
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'fine image'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
