import setup_path
import airviz 
import time
import threading

def echo(clisrv, obj):
    clisrv.send_obj("Hellooo " + str(obj))

def setup_clisrv():
    cli_ser1 = airviz.ZmqPubSub.ClientServer(12332, True, callback=echo)
    airviz.ZmqPubSub.run_forever()

srv1 = airviz.ZmqPubSub.Publication(12333)
srv2 = airviz.ZmqPubSub.Publication(12334)

th = threading.Thread(target=setup_clisrv, daemon=True)
th.start()

for i in range(10000):
    srv1.send_obj((i, i*i), "ch1")
    srv1.send_obj((i, i*i*2), "ch2")
    srv2.send_obj((i, i*i*i), "ch1")
    time.sleep(5)