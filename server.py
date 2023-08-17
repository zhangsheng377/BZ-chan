import logging
import os

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer

from UTILS.channel import ChannelFactory
from UTILS.db_sheets import get_bz_chan

app = Flask(__name__)

PORT = int(os.getenv('PORT'))


@app.route("/", methods=['POST', 'GET'])
def hello_world():
    return "hello_world"


def request_parse(req_data):
    """解析请求数据并以json形式返回"""
    if req_data.method == 'POST':
        return req_data.json
    elif req_data.method == 'GET':
        return req_data.args
    return {}


@app.route("/<send_key>.send", methods=['POST', 'GET'])
def handle(send_key):
    bz_chan = get_bz_chan(send_key)
    if not bz_chan or 'channel' not in bz_chan:
        return f'send_key:{send_key} error.', 404
    data = request_parse(request)
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    app.logger.info(data)

    msg_type = data.pop('msg_type', 'markdown')

    channel_name = bz_chan['channel']
    channel = ChannelFactory.get(channel_name=channel_name)
    post_args = channel.get_post_args(send_key=send_key, msg_type=msg_type, **data)
    r = requests.post(**post_args)
    return r.text


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    http_server = WSGIServer(('0.0.0.0', PORT), app)
    http_server.serve_forever()
