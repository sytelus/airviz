import setup_path
from airviz import ZmqPubSub
import time

srv1 = ZmqPubSub.Publication(12333)
srv2 = ZmqPubSub.Publication(12334)

for i in range(10000):
    srv1.send_obj((i, i*i), "ch1")
    srv1.send_obj((i, i*i*2), "ch2")
    srv2.send_obj((i, i*i*i), "ch1")
    time.sleep(1)