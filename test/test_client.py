import setup_path
from airviz import ZmqPubSub

cli = ZmqPubSub()
sub = cli.start_sub(12333, topic = "ch1")

for i in range(10000):
    o = sub.recv()
    print(o)

