import setup_path
import airviz 
import time

watcher = airviz.Watch()

for i in range(10000):
    watcher.send_text("Epoch: " + str(i))
    time.sleep(1)
