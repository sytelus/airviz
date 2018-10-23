import zmq
import pickle
from zmq.eventloop import ioloop, zmqstream
import threading
import functools

class ZmqPubSub:
    class Publication:
        def __init__(self, port, host="*"):
            context = zmq.Context()
            self._socket = context.socket(zmq.PUB)
            self._socket.bind("tcp://%s:%d" % (host, port))

        def send_obj(self, obj, topic=""):
            self._socket.send_multipart([topic.encode(), pickle.dumps(obj)])

    class Subscription:
        def __init__(self, port, topic="", callback=None, host="localhost"):
            if callback is not None:
                self._thread = threading.Thread(target=self._start, kwargs=dict(port=port, topic=topic, callback=callback, host=host))
                self._thread.daemon = True
                self._thread.start()
            else:
                self._thread = None
                _start(port=port, topic=topic, callback=callback, host=host)

        def _callback_wrapper(self, callback, msg):
            [topic, obj_s] = msg
            callback(pickle.loads(obj_s))

        def _start(self, port, topic="", callback=None, host="localhost"):
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
                self._ioloop = ioloop.IOLoop.current()
                self._ioloop.start()
            else:
                self._ioloop = None

        def stop():
            self._ioloop.stop()

        def join(self):
            if self._thread is not None:
                self._thread.join()

        def receive_obj(self):
            [topic, obj_s] = self._socket.recv_multipart()
            if topic != self.topic:
                raise ValueError("Expected topic: %s, Received topic: %s" % (topic, self.topic)) 
            return pickle.loads(obj_s)

    class Server:
        def __init__(self, port, callback=None, host="*"):
            if callback is not None:
                self._thread = threading.Thread(target=self._start, kwargs=dict(port=port, callback=callback, host=host))
                self._thread.daemon = True
                self._thread.start()
            else:
                self._thread = None
                _start(port=port, callback=callback, host=host)

        def _start(self, port, callback=None, host="*"):
            def callback_wrapper(callback, msg):
                [topic, obj_s] = msg
                callback(pickle.loads(obj_s))

            context = zmq.Context()
            self._socket = context.socket(zmq.REP)
            self._socket.bind("tcp://%s:%d" % (host, port))
            if callback is not None:
                self._stream = zmqstream.ZMQStream(self._socket)
                wrapper = functools.partial(callback_wrapper, callback)
                self._stream.on_recv(wrapper)
                self._ioloop = ioloop.IOLoop.current()
                self._ioloop.start()
            else:
                self._ioloop = None

        def join(self):
            if self._thread is not None:
                self._thread.join()

        def stop():
            self._ioloop.stop()

        def send_obj(self, obj):
            self._socket.send(pickle.dumps(obj))

    class Client:
        def __init__(self, port, host = "*"):
            context = zmq.Context()
            self._socket = context.socket(zmq.REQ)
            self._socket.connect("tcp://%s:%d" % (host, port))

        def receive_obj(self):
            obj_s = self._socket.recv()
            return pickle.loads(obj_s)

    def create_pub(self, port, host="*"):
        return ZmqPubSub.Publication(port, host)

    def create_sub(self, port, topic="", host="localhost"):
        return ZmqPubSub.Subscription(port, topic, host)




