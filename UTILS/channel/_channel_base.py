from abc import ABC, abstractmethod


class Channel(ABC):
    @abstractmethod
    def _get_webhook(self, send_key: str):
        raise NotImplementedError

    @abstractmethod
    def get_post_args(self, send_key: str, msg_type: str, **kwargs):
        raise NotImplementedError
