import logging

from ._channel_base import Channel


class ChannelFactory:
    _map = {}

    @staticmethod
    def register(channel_name: str, channel_class):
        ChannelFactory._map[channel_name] = channel_class
        logging.info(f"ChannelFactory : register_channel : channel_name:{channel_name} channel_class:{channel_class}")

    @staticmethod
    def get(channel_name: str, *args, **kwargs) -> Channel:
        channel_class = ChannelFactory._map.get(channel_name, None)
        if channel_class is None:
            logging.error(f"ChannelFactory : get : channel_name:{channel_name} is invalid.")
            return None

        return channel_class(*args, **kwargs)
