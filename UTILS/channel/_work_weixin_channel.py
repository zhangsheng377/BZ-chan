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
    TEMPLATE_CARD_NEWS_NOTICE = 'template_card_news_notice'


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
    return {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }


def _get_file_message(send_key: str, file_path: str = 'README.md', proxies=None, *args, **kwargs):
    if proxies is None:
        proxies = {}
    up_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={send_key}&type=file"
    file_data = open(file_path, "rb")
    file = {os.path.basename(file_path): file_data}
    res = requests.post(up_file_url, files=file, proxies=proxies)  # 需要先将文件上传到腾讯的临时文件服务器
    media_id = res.json()['media_id']
    return {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }


def _get_template_card_news_notice_message(rss_feed_title: str, url: str, title: str, last_title: str, image_url: str,
                                           *args, **kwargs):
    return {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "news_notice",
            "source": {
                "desc": f"{rss_feed_title}",
            },
            "main_title": {
                "title": f"{title}",
            },
            "card_image": {
                "url": f"{image_url}",
            },
            "quote_area": {
                "type": 1,
                "url": f"{url}",
                "quote_text": f"<-- {last_title}"
            },
            "jump_list": [
                {
                    "type": 1,
                    "url": f"{url}",
                    "title": "详情链接"
                },
            ],
            "card_action": {
                "type": 1,
                "url": f"{url}",
            }
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
            message = _get_file_message(send_key=send_key, proxies=self.proxies, *args, **kwargs)
        elif msg_type == MsgType.TEMPLATE_CARD_NEWS_NOTICE:
            message = _get_template_card_news_notice_message(*args, **kwargs)
        else:
            raise NotImplementedError

        message_json = json.dumps(message)
        webhook = self._get_webhook(send_key=send_key)
        return {'url': webhook, 'data': message_json, 'headers': self.header, 'proxies': self.proxies}


ChannelFactory.register(channel_name='企业微信', channel_class=WorkWeixinChannel)
