from .zmq_pub_sub import ZmqPubSub

class Probe:
    def __init__(self, port = 40859, host="localhost"):
        self._port = port
        self._host = host
        self._clients = {}

    def stream(self, expression, event_name, stream_name):
        self._clients[stream_name] = ZmqPubSub().start_sub(self._port, stream_name, self._host)
        self._clients[stream_name]