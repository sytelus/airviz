import zmq
import pickle
from zmq.eventloop import ioloop, zmqstream
import functools
import threading

class ZmqPubSub:
    @staticmethod
    def run_forever():
        ioloop.IOLoop.current().start()

    class Publication:
        def __init__(self, port, host="*"):
            context = zmq.Context()
            self._socket = context.socket(zmq.PUB)
            self._socket.bind("tcp://%s:%d" % (host, port))

        def send_obj(self, obj, topic=""):
            self._socket.send_multipart([topic.encode(), pickle.dumps(obj)])

    class Subscription:
        def __init__(self, port, topic="", callback=None, host="localhost"):
            def callback_wrapper(callback, msg):
                [topic, obj_s] = msg
                callback(pickle.loads(obj_s))

            context = zmq.Context()
            self.topic = topic.encode()
            self._socket = context.socket(zmq.SUB)
            self._socket.connect("tcp://%s:%d" % (host, port))
            if topic != "":
                self._socket.setsockopt(zmq.SUBSCRIBE, self.topic)
            if callback is not None:
                self._stream = zmqstream.ZMQStream(self._socket)
                wrapper = functools.partial(callback_wrapper, callback)
                self._stream.on_recv(wrapper)
            #else use receive_obj

        def _callback_wrapper(self, callback, msg):
            [topic, obj_s] = msg
            callback(pickle.loads(obj_s))

        def receive_obj(self):
            [topic, obj_s] = self._socket.recv_multipart()
            if topic != self.topic:
                raise ValueError("Expected topic: %s, Received topic: %s" % (topic, self.topic)) 
            return pickle.loads(obj_s)

    class SubscriptionManager:
        def __init__(self, port = None):
            self._port = port
            self._thread = threading.Thread(target=self._run_subs, daemon=True)
            self._thread.start()

        def _run_subs(self):
            ZmqPubSub.run_forever()

        def add_sub(self, callback, topic="", port=None):
            ioloop.IOLoop.current().add_callback( \
                lambda : ZmqPubSub.Subscription(port or self._port, topic=topic, callback=callback))

    class ClientServer:
        def __init__(self, port, is_server, callback=None, host=None):
            def callback_wrapper(callback, msg):
                [obj_s] = msg
                callback(self, pickle.loads(obj_s))

            context = zmq.Context()
            if is_server:
                host = host or "*"
                self._socket = context.socket(zmq.REP)
                self._socket.bind("tcp://%s:%d" % (host, port))
            else:
                host = host or "localhost"
                self._socket = context.socket(zmq.REQ)
                self._socket.connect("tcp://%s:%d" % (host, port))

            if callback is not None:
                self._stream = zmqstream.ZMQStream(self._socket)
                wrapper = functools.partial(callback_wrapper, callback)
                self._stream.on_recv(wrapper)
            #else use receive_obj

        def send_obj(self, obj):
            self._socket.send_multipart([pickle.dumps(obj)])

        def receive_obj(self):
            [obj_s] = self._socket.recv_multipart()
            return pickle.loads(obj_s)
