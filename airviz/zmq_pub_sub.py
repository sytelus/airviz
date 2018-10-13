import zmq
import pickle

class ZmqPubSub:
    class Subscription:
        def __init__(self, port, topic="", host="localhost"):
            context = zmq.Context()
            self.topic = topic.encode()
            self.sub = context.socket(zmq.SUB)
            self.sub.connect("tcp://%s:%d" % (host, port))
            if topic != "":
                self.sub.setsockopt(zmq.SUBSCRIBE, self.topic)

        def recv(self):
            [topic, obj_s] = self.sub.recv_multipart()
            if topic != self.topic:
                raise ValueError("Expected topic: %s, Received topic: %s" % (topic, self.topic)) 
            return pickle.loads(obj_s)

    def start_pub(self, port, host="*"):
        context = zmq.Context()
        self.pub = context.socket(zmq.PUB)
        self.pub.bind("tcp://%s:%d" % (host, port))

    def start_sub(self, port, topic="", host="localhost"):
        return ZmqPubSub.Subscription(port, topic, host)

    def send(self, obj, topic=""):
        self.pub.send_multipart([topic.encode(), pickle.dumps(obj)])


