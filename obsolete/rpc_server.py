from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread

class RpcServer(SimpleXMLRPCServer):
    def __init__(self, port, host = None):
        import socket
        super(SimpleXMLRPCServer, self).__init__((host or socket.gethostbyname(), port))
        self._server_thread = None

    def start(self):
        if (self.server_thread):
            return 
            
        self._server_thread = Thread(target=self._serve)
        self._server_thread.start()

    def stop(self):
        if (not self.server_thread):
            return 
        self.shutdown()
        self._server_thread.join()

    def _serve(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()
