import json
from enum import Enum

from ._factory import ChannelFactory
from ._channel_base import Channel


# https://sct.ftqq.com/

class MsgType(Enum):
    MARKDOWN = 'markdown'


def _get_markdown_message(title: str, desp: str, *args, **kwargs):
    return {
        'title': title,
        'desp': desp
    }


class ServerChanChannel(Channel):
    def __init__(self, header=None, proxies=None):
        super(ServerChanChannel, self).__init__()
        self.header = header if header is not None else {"Content-Type": "application/json"}
        self.proxies = proxies if proxies is not None else {}

    def _get_webhook(self, send_key: str):
        return f"https://sctapi.ftqq.com/{send_key}.send"

    def get_post_args(self, send_key: str, msg_type: str, *args, **kwargs):
        msg_type = MsgType(msg_type)
        if msg_type == MsgType.MARKDOWN:
            message = _get_markdown_message(*args, **kwargs)
        else:
            raise NotImplementedError

        message_json = json.dumps(message)
        webhook = self._get_webhook(send_key=send_key)
        return {'url': webhook, 'data': message_json, 'headers': self.header, 'proxies': self.proxies}


ChannelFactory.register(channel_name='Server酱', channel_class=ServerChanChannel)
