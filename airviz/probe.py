from .zmq_pub_sub import ZmqPubSub

class Probe:
    def _on_recv_default_topic(self, text):
        print(text)

    def __init__(self, port = 40859, host="localhost"):
        self._port = port
        self._host = host
        self._subscriptions = {}
        self._subscriptions[""] = ZmqPubSub.Subscription(port=self._port, host=host, callback=self._on_recv_default_topic)

    def stream(self, expression, event_name, stream_name):
        self._clients[stream_name] = ZmqPubSub().start_sub(self._port, stream_name, self._host)
        self._clients[stream_name]