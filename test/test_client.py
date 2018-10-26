import setup_path
import airviz
import threading
import time

def sub_recvd_srv1_ch1(obj):
    print("srv1, ch1", end =" - ")
    print(obj)

def sub_recvd_srv1_ch2(obj):
    print("srv1, ch2", end =" - ")
    print(obj)

def sub_recvd_srv2_ch1(obj):
    print("srv1, ch1", end =" - ")
    print(obj)


mgr = airviz.ZmqPubSub.SubscriptionManager(12333)
mgr.add_sub(sub_recvd_srv1_ch1, "ch1")
mgr.add_sub(sub_recvd_srv1_ch2, "ch2")
mgr.add_sub(sub_recvd_srv2_ch1, "ch1", port=12334)


cli_ser1 = airviz.ZmqPubSub.ClientServer(12332, False)
for i in range(0, 1000):
    cli_ser1.send_obj("Hello " + str(i))
    resp = cli_ser1.receive_obj()
    print(resp)
    time.sleep(1)

airviz.wait_key()



