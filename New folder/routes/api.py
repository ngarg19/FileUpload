import flask
import os
import hashlib

from myutils.config import Config

blueprint = flask.Blueprint('api', __name__)

@blueprint.route("/api/upload", methods=['POST'])
def upload_file():

    if "file" not in flask.request.files:
        return flask.jsonify({'error': 'no file'}), 400

    file = flask.request.files['file']
    if file.filename == '':
        return flask.jsonify({'error': 'no file selected'}), 400

    if os.path.exists(os.path.join(Config.get_upload_dir(), file.filename)):
        return flask.jsonify({'error': 'file already exists'}), 409

    if file:
        filename = file.filename
        file.save(os.path.join(Config.get_upload_dir(), filename))        
        link = "/view/" + os.path.join(Config.get_upload_dir(), filename).replace(Config.get_upload_dir(), "")
        return flask.jsonify({'link': link}), 200        
        
    return flask.jsonify({'error': 'unknown error'}), 500

