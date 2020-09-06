import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import encoder

"""
Build commands:
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
"""

UPLOAD_FOLDER = 'media/'
PROCESSED_FOLDER = 'media/processed/'

ALLOWED_EXTENSIONS = {"audio_extensions": ["mp3", "wav", "aiff", "m4a"],
                      "image_extensions": ["jpg", "jpeg", "png"]}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER


def allowed_file(filename):
    if '.' in filename:
        file_extension = filename.rsplit('.', 1)[1].lower()
        if file_extension in ALLOWED_EXTENSIONS["audio_extensions"]:
            return "audio"
        elif file_extension in ALLOWED_EXTENSIONS["image_extensions"]:
            return "image"
    else:
        return False


def process_files(uploaded_files):

    fileset = {"audio_files": [],
               "image_file": "file.jpg"}

    for file in uploaded_files:

        file_is_allowed = allowed_file(file.filename)
        if file and file_is_allowed:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if file_is_allowed is "audio":
                fileset["audio_files"].append(file_path)
            elif file_is_allowed is "image":
                fileset["image_file"] = file_path

    return fileset


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        processed_files = process_files(uploaded_files)
        if processed_files:
            return render_template('index.html', selected=uploaded_files)

        encoded_video_files = (encoder.encode_video_new(processed_files))

        if encoded_video_files:
            return render_template('uploads.html', filenames=encoded_video_files)
        else:
            return render_template('index.html', error="No Files selected")


    return render_template('index.html', )


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'],
                               filename)
