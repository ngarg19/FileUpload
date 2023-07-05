import flask
import os
import datetime
import hashlib

from myutils.file import File, human_readable_size
from myutils.config import Config

blueprint = flask.Blueprint('general', __name__)


@blueprint.route('/', methods=['GET'])
def files():

    files = []
    # for file in os.listdir(Config.get_upload_dir()):
    #     file_path = "/view/" + os.path.join(Config.get_upload_dir(), file).replace(Config.get_upload_dir(), "")
    #     file_delete_path = file_path.replace("/view/", "/delete/")
    #     file_rename_path = file_path.replace("/view/", "/rename/")
    #     file_extension = os.path.splitext(file)[1]
    #     file_date = os.path.getmtime(os.path.join(Config.get_upload_dir(), file))
    #     file_date = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
    #     file_size = os.path.getsize(os.path.join(Config.get_upload_dir(), file))
    #     file_size = human_readable_size(file_size)

    #     files.append(File(file_extension, file_path, file_delete_path, file_rename_path, file, file_date, file_size))

    return flask.render_template('files.html', files=files, auth_token_hash=hashlib.md5(Config.get_auth_token().encode('utf-8')).hexdigest(), default_auth_token_hash="b0439fae31f8cbba6294af86234d5a28")