import logging

from ._channel_base import Channel


class ChannelFactory:
    _channel_map = {}

    @staticmethod
    def register_channel(channel_name: str, channel_class):
        ChannelFactory._channel_map[channel_name] = channel_class
        print(f"ChannelFactory : register_channel : channel_name:{channel_name} channel_class:{channel_class}")

    @staticmethod
    def get(channel_name: str, **kwargs) -> Channel:
        channel_class = ChannelFactory._channel_map.get(channel_name, None)
        if channel_class is None:
            logging.error(f"ChannelFactory : get : channel_name:{channel_name} is invalid.")
            return None

        return channel_class(**kwargs)
