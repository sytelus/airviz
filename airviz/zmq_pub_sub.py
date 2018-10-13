import zmq
import pickle

class ZmqPubSub:
    class Subscription:
        def __init__(self, port, channel="", host="localhost"):
            context = zmq.Context()
            self.channel = channel.encode()
            self.sub = context.socket(zmq.SUB)
            self.sub.connect("tcp://%s:%d" % (host, port))
            if channel != "":
                self.sub.setsockopt(zmq.SUBSCRIBE, self.channel)

        def recv(self):
            [channel, obj_s] = self.sub.recv_multipart()
            if channel != self.channel:
                raise ValueError("Expected channel: %s, Received channel: %s" % (channel, self.channel)) 
            return pickle.loads(obj_s)

    def start_pub(self, port, host="*"):
        context = zmq.Context()
        self.pub = context.socket(zmq.PUB)
        self.pub.bind("tcp://%s:%d" % (host, port))

    def start_sub(self, port, channel="", host="localhost"):
        return ZmqPubSub.Subscription(port, channel, host)

    def send(self, obj, channel=""):
        self.pub.send_multipart([channel.encode(), pickle.dumps(obj)])


