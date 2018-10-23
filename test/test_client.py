import setup_path
import airviz

def sub_recvd_srv1_ch1(obj):
    print("srv1, ch1", end =" - ")
    print(obj)
def sub_recvd_srv1_ch2(obj):
    print("srv1, ch2", end =" - ")
    print(obj)

airviz.add_windows_ctrl_c()
cli1 = airviz.ZmqPubSub.Subscription(12333, topic = "ch1", callback=sub_recvd_srv1_ch1)
#cli2 = airviz.ZmqPubSub.Subscription(12333, topic = "ch2", callback=sub_recvd_srv1_ch2)
cli1.join()
#cli2.join()

