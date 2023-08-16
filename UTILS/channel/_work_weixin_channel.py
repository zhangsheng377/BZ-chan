import json
from enum import Enum

from ._factory import ChannelFactory
from ._channel_base import Channel


class MsgType(Enum):
    MARKDOWN = 'markdown'


class WorkWeixinChannel(Channel):
    def __init__(self, msg_type, header=None, proxies=None):
        super(WorkWeixinChannel, self).__init__(msg_type=msg_type)
        self.msg_type = MsgType(msg_type)
        self.header = header if header is not None else {"Content-Type": "application/json"}
        self.proxies = proxies if proxies is not None else {}

    def _get_webhook(self, send_key: str):
        return f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={send_key}"

    def get_post_args(self, send_key: str, msg: str):
        if self.msg_type == MsgType.MARKDOWN:
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "content": msg
                }
            }
            message_json = json.dumps(message)
            webhook = self._get_webhook(send_key=send_key)
            return {'url': webhook, 'data': message_json, 'headers': self.header, 'proxies': self.proxies}
        else:
            raise NotImplementedError


ChannelFactory.register_channel(channel_name='企业微信', channel_class=WorkWeixinChannel)
