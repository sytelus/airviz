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


def run_subs():
    cli1 = airviz.ZmqPubSub.Subscription(12333, topic = "ch1", callback=sub_recvd_srv1_ch1)
    cli2 = airviz.ZmqPubSub.Subscription(12333, topic = "ch2", callback=sub_recvd_srv1_ch2)
    cli3 = airviz.ZmqPubSub.Subscription(12334, topic = "ch1", callback=sub_recvd_srv2_ch1)

    airviz.ZmqPubSub.run_forever()

th = threading.Thread(target=run_subs, daemon=True)
th.start()

cli_ser1 = airviz.ZmqPubSub.ClientServer(12332, False)
for i in range(0, 1000):
    cli_ser1.send_obj("Hello " + str(i))
    resp = cli_ser1.receive_obj()
    print(resp)
    time.sleep(1)

airviz.wait_key()



