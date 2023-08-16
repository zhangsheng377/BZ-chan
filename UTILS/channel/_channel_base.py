from abc import ABC, abstractmethod


class Channel(ABC):
    def __init__(self, msg_type):
        self.msg_type = msg_type

    @abstractmethod
    def _get_webhook(self, send_key: str):
        raise NotImplementedError

    @abstractmethod
    def get_post_args(self, send_key: str, msg: str):
        raise NotImplementedError
