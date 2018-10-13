class Server:
    def __init__(self, port = 40859):
        self.server = RpcServer(40859)
        self.server.start()
        self._watched = {}
        self._events = {}

    def watch(**vars):
        self._watched.update(vars)

    def occured(*event_names):
        for event_name in event_names:
            self._events[event_name] = self._events.get(event_name, 0) + 1
