import zmq
import pickle

class ZmqPubSub:
    _poller = zmq.Poller()

    class Publication:
        def __init__(self, port, host="*"):
            context = zmq.Context()
            self.z = context.socket(zmq.PUB)
            self.z.bind("tcp://%s:%d" % (host, port))
            ZmqPubSub._poller.register(self.z, zmq.POLLIN)

        def send_obj(obj, topic=""):
            self.z.send_multipart([topic.encode(), pickle.dumps(obj)])

    class Subscription:
        def __init__(self, port, topic="", host="localhost"):
            context = zmq.Context()
            self.topic = topic.encode()
            self.z = context.socket(zmq.SUB)
            self.z.connect("tcp://%s:%d" % (host, port))
            if topic != "":
                self.z.setsockopt(zmq.SUBSCRIBE, self.topic)

        def receive_obj(self):
            [topic, obj_s] = self.z.recv_multipart()
            if topic != self.topic:
                raise ValueError("Expected topic: %s, Received topic: %s" % (topic, self.topic)) 
            return pickle.loads(obj_s)

    class Server:
        def __init__(self, port, host="*"):
            context = zmq.Context()
            self.z = context.socket(zmq.REP)
            self.z.bind("tcp://%s:%d" % (host, port))
            ZmqPubSub._poller.register(self.z, zmq.POLLIN)

        def send_obj(obj):
            self.z.send(pickle.dumps(obj))

    class Client:
        def __init__(self, port, host="*"):
            context = zmq.Context()
            self.z = context.socket(zmq.REQ)
            self.z.connect("tcp://%s:%d" % (host, port))

        def receive_obj(self):
            obj_s = self.z.recv()
            return pickle.loads(obj_s)

    def create_pub(self, port, host="*"):
        return ZmqPubSub.Publication(port, host)

    def create_sub(self, port, topic="", host="localhost"):
        return ZmqPubSub.Subscription(port, topic, host)




