import os
from flask import Flask, render_template, url_for, request, jsonify
from werkzeug import secure_filename
from tempfile import mkdtemp
from putzcard.face_detect import find_faces

UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER'] if 'UPLOAD_FOLDER' in os.environ else mkdtemp()

app = Flask(__name__)

app.config['DEBUG'] = bool(os.environ.get('DEBUG'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.filters['static'] = lambda name: url_for('static', filename=name)

@app.route('/')
def index():
    return render_template('index.tmpl')

@app.route('/putzcard_maker/')
def drop_test():
    return render_template('putzcard_maker.tmpl')

@app.route('/face_upload', methods=['POST'])
def upload_for_detect():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(file_save_path)
        cascade_file_path = os.path.join(app.root_path, 'deps/opencv/haarcascade_frontalface_default.xml')
        image, faces = find_faces(file_save_path, cascade_file_path)
        if not faces:
            face = False
        else:
            face = {}
            face['x'], face['y'], face['height'], face['width'] = faces[0][0]
        return jsonify({'image' : image, 'face' : face})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
