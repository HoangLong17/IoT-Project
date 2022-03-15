import paho.mqtt.client as mqtt
import base64
import time

if __name__=="__main__":
	broker_address="192.168.1.68" 
	client = mqtt.Client()
	client.connect(broker_address)
	client.loop_start() #start the loop
	root = "demo_image/data"
	count = 0
	ctime = time.time()
	while True:
		for i in range(229):
			path = "demo_image/data/frame{}.jpg".format(i)
			with open(path, "rb") as image:
				message = base64.b64encode(image.read())
			client.publish("esp32/cam_1", message, qos=2)
			time.sleep(0.05)
			count += 1
			print("Image pushed at {} frames/s".format(count/(time.time()-ctime)))
	time.sleep(4) # wait
	client.loop_stop() #stop the loop
