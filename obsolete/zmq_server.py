from zeroless import Server

class ZmqServer:
    def start(self, port):
        self._server = Server(port=port)
        self.pubs = {}

    def send(self, obj, topic):
        if not topic in self.pubs:
            self.pubs[topic] = self._server.pub(topic=topic, embed_topic=True)
        self.pubs[topic](obj)