import json
import os.path
import re
from enum import Enum

import requests

from ._factory import ChannelFactory
from ._channel_base import Channel


# https://developer.work.weixin.qq.com/document/path/99110

class MsgType(Enum):
    MARKDOWN = 'markdown'
    TEXT = 'text'
    NEWS = 'news'
    FILE = 'file'


def _get_markdown_message(content: str, *args, **kwargs):
    return {
        "msgtype": "markdown",
        "markdown": {
            "content": content,
            "mentioned_list": ["balabala", "@all"],
            "mentioned_mobile_list": ["139********", "@all"]
        }
    }


def _get_text_message(content: str, mentioned_list: list = None, mentioned_mobile_list: list = None, *args, **kwargs):
    return {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list,
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }


def _get_news_message(articles: list, *args, **kwargs):
    str1 = articles[0]['picurl']
    pattern = re.compile("""<img[^>]+src=["']([^'"<>]+)["'][^<>]+/?>""")  # 要有空格隔开 才会有输出结果
    str2 = pattern.findall(str1)
    print(str2)
    if len(str2) > 0:
        articles[0]['picurl'] = str2[0]
    return {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }


class WorkWeixinChannel(Channel):
    def __init__(self, header=None, proxies=None):
        super(WorkWeixinChannel, self).__init__()
        self.header = header if header is not None else {"Content-Type": "application/json"}
        self.proxies = proxies if proxies is not None else {}

    def _get_webhook(self, send_key: str):
        return f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={send_key}"

    def get_post_args(self, send_key: str, msg_type: str, *args, **kwargs):
        msg_type = MsgType(msg_type)
        if msg_type == MsgType.MARKDOWN:
            message = _get_markdown_message(*args, **kwargs)
        elif msg_type == MsgType.TEXT:
            message = _get_text_message(*args, **kwargs)
        elif msg_type == MsgType.NEWS:
            message = _get_news_message(*args, **kwargs)
        elif msg_type == MsgType.FILE:
            message = self._get_file_message(send_key=send_key, *args, **kwargs)
        else:
            raise NotImplementedError
        message_json = json.dumps(message)
        webhook = self._get_webhook(send_key=send_key)
        return {'url': webhook, 'data': message_json, 'headers': self.header, 'proxies': self.proxies}

    def _get_file_message(self, send_key: str, file_path: str = 'README.md', *args, **kwargs):
        up_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={send_key}&type=file"
        file_data = open(file_path, "rb")
        file = {os.path.basename(file_path): file_data}
        res = requests.post(up_file_url, files=file, proxies=self.proxies)  # 需要先将文件上传到腾讯的临时文件服务器
        media_id = res.json()['media_id']
        return {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }


ChannelFactory.register(channel_name='企业微信', channel_class=WorkWeixinChannel)
