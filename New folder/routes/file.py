import flask
import os
import datetime
from flask import redirect

from myutils.config import Config
from myutils.file import File, human_readable_size

blueprint = flask.Blueprint('file', __name__)
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."


import requests

headers = {
    'Authorization': 'Bearer f93ce61f87965d1f1fe44c03c66ec259fd4b0221',
    'Content-Type': 'application/json',
}

def getShortLink(url):

    complete_url = Config.get_server()+url

    data = '{ "long_url": "'+complete_url+'"}'

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)

    print(response)
    try:
        shortened_url = response.json()
        print(shortened_url)
        return shortened_url['link']
    except:
        return complete_url

@blueprint.route('/view/<path:path>')
def get_file(path):

    file_path = os.path.join(Config.get_upload_dir(), path)
    if not os.path.isfile(file_path):
        return flask.jsonify({'error': 'file does not exist'}), 404

    file_delete_path = file_path.replace("files/", "/delete/")
    file_rename_path = file_path.replace("files/", "/rename/")
    file_extension = os.path.splitext(file_path)[1]
    file_date = os.path.getmtime(file_path)
    file_date = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
    file_size = os.path.getsize(file_path)
    file_size = human_readable_size(file_size)
    fileLink = getShortLink("/view/"+path)
    downloadLink = getShortLink("/view/raw/"+path)
    
    file = File(file_extension, file_path.replace("files/", "/view/raw/"), file_delete_path, file_rename_path, file_path.replace("files/", ""), file_date, file_size,downloadLink,fileLink)
    

    return flask.render_template('view.html', file=file, auth_token="")

@blueprint.route('/view/raw/<path:path>')
def get_raw_file(path):
    file_path = os.path.join(Config.get_upload_dir(), path)
    if not os.path.isfile(file_path):
        return flask.jsonify({'error': 'file does not exist'}), 404

    print(file_path)

    return flask.send_file(file_path)

@blueprint.route('/rename/<path:path>', methods=['POST'])
def rename_file(path):

    file_path = os.path.join(Config.get_upload_dir(), path)
    if not os.path.isfile(file_path):
        return flask.jsonify({'error': 'file does not exist'}), 404

    new_name = flask.request.json["new_name"]
    if not new_name:
        return flask.jsonify({'error': 'no new name'}), 400

    if not all(c in allowed_chars for c in new_name):
        return flask.jsonify({'error': 'invalid characters in name'}), 400

    os.rename(file_path, os.path.join(Config.get_upload_dir(), new_name))
    return flask.jsonify({'success': True}), 200

@blueprint.route('/delete/<path:path>')
def delete_file(path):

    try:
        os.remove(os.path.join(Config.get_upload_dir(), path))
        return redirect("/")
        
    except FileNotFoundError: return flask.jsonify({'error': 'file not found'}), 404
    except PermissionError: return flask.jsonify({'error': 'permission denied'}), 403
    except Exception as e: return flask.jsonify({'error': str(e)}), 500

