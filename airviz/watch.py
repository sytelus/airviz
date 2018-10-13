from .zmq_pub_sub import ZmqPubSub

class Watch:
    class Stream:
        def __init__(self, expression, event_name, stream_name):
            self.expression = expression
            self.event_name = event_name
            self.stream_name = stream_name

    def __init__(self, port = 40859):
        self._server = ZmqPubSub()
        self._server.start_pub(port)
        self._vars = {}
        self._event_counts = {}
        self._streams = {}

    def register(self, var_name, var_value):
        self._vars[var_name] = var_value

    def unregister(self, var_name):
        self.watched.pop(var_name, None)

    def occured(self, event_name):
        self._event_counts[event_name] = self._event_counts.get(event_name, 0) + 1
        event_streams = self._streams.get(event_name, {})
        for stream_name, s in event_streams:
            val = eval(s.expression, self._vars)
            self._server.send((val, self._event_counts[event_name]), stream_name)

    def stream(self, expression, event_name, stream_name):
        s = Watch.Stream(expression, event_name, stream_name)
        event_streams[stream_name] = s

    def destream(self, event_name, stream_name):
        event_streams = self._streams.get(s.event_name, {})
        event_streams.pop(stream_name, None)