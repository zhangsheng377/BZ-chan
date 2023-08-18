FROM zhangsheng377/ubuntu:latest
# ENTRYPOINT []

# RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pymongo requests flask gevent redis

RUN git clone --recursive https://github.com/zhangsheng377/BZ-chan.git --depth=1

WORKDIR /BZ-chan

# CMD ["/bin/bash"]
