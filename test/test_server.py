import setup_path
from airviz import ZmqPubSub
import time

srv = ZmqPubSub()
srv.start_pub(12333)

for i in range(10000):
    srv.send((i, i*i), "ch1")
    time.sleep(1)