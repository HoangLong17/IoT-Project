import queue
import time
from .tasks import face_ai
from .models import Student, Class, Authentication
import paho.mqtt.client as mqtt
import time
import base64
import cv2
from datetime import date


class VideoBase():
	def __init__(self):
		self.Class = "-1"
		self.queue = queue.Queue()
		self.start_time = time.time()
		self.con = False
	
	def connect(self):
		self.con = True
		self.note("connect . .  .")
		self.note("connect successfully!")
		return True 
	def disconnect(self):
		self.con = False
		self.note("disconnect . .  .")
		self.note("disconnect successfully!")
		return True

	def capture(self):
		#self.test_DB()
		return "Viet Pham", [1,2,3,4]

	def stream(self):
		file_name = "media/background.png"
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n') 

	def note(self, message):
		print(message)

	def listStudent(self, pk):
		if Class.objects.filter(value=pk).exists():
			c = Class.objects.get(value=pk)
			l = []
			if Authentication.objects.filter(date = date.today()).exists():
				print('today:', date.today())
			Auth = Authentication.objects.filter(date = date.today())
			for student in Student.objects.filter(Class=c):
				for aut in Auth:
					print(student.name, aut.student)
					if str(student.name) == str(aut.student):
						print("true")
						student.status = aut.status
				l.append(student)
			return l

	def updateAuthentication(self,mssv):
		if Student.objects.filter(mssv=mssv).exists():

			# If 'mssv' exists, then matched and get
			student = Student.objects.get(mssv=mssv)

			# Then save the 'username' into Authentication table into database
			Authentication.objects.get_or_create(
				student=student,
				status=True,
				date = date.today()
			)
			return True
		return False

	def test_DB(self):
		students = Student.objects.filter(Class=self.Class)
		print(self.Class)
		for std in students:
			std.status = 1-std.status
			std.save()

class VideoDemo(VideoBase):
	def __init__(self):
		super().__init__() 
		self.Class = "0"

	def stream(self):
		if self.con == False:
			file_name = "media/background.png"
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
		else:
			j = 0
			while True:
				time.sleep(0.05)
				j = j%7 +1
				# print(j)
				file_name = 'media/HoangLong/'+str(j)+'.JPG'
				yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')       
		
	def capture(self):
		name, box= face_ai('media/demo.jpg') 
		self.note("get get get")
		# self.test_DB()
		# if name != 'Unknown':
		#     # self.updateStudent(name, 1)
		return name, box

	
class VideoApp(VideoBase):
	def __init__(self, topic):
		super().__init__() 
		self.topic = topic
		self.Class = "1"
		self.img_received = False
		self.client = None
		self.file_name = "media/imageToSave.png"
		self.file_output = "media/output.jpg"
		self.showbox = False
		self.current = 0
		self.c_capture = True
		self.images = 0
	
	def connect(self):
		self.con = True
		self.note("connect . .  .")
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect("192.168.1.68", 1883)
		self.client.loop_start()
		self.note("connect successfully!")
		return True 

	def disconnect(self):
		self.con = False
		self.client.loop_stop()
	
	def stream(self):
		if self.con == False:
			file_name = "media/background.png"
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
		else:
			ctime = time.time()
			while True:
				if self.showbox == True:
					yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_output, 'rb').read() + b'\r\n')
					if time.time() - self.current > 2:
						self.showbox = False
						self.current = 0
						self.c_capture = True
				else:
					try:
						if self.img_received:
							#print("Image received")
							self.images += 1
							print("Image recrived at {} frames/s".format(self.images/(time.time()-ctime)))
							self.img_received = False

							yield (b'--frame\r\n'
								b'Content-Type: image/jpeg\r\n\r\n' + self.payload  + b'\r\n')  #open(file_name, 'rb').read()
					except Exception as e:
						print(e)


	def capture(self):
		with open(self.file_name, "wb") as fh:
			fh.write(self.payload)
		if self.c_capture:
			self.c_capture = False
			name, box= face_ai(self.file_name) 
			self.note("get get get")
			self.updateAuthentication(name[0])
			if len(name)!=0:
				self.showbox = True
				self.current = time.time()
			else:
				name.append("Unknown")
				self.c_capture = True
			return name, box
		else:
			return ['Waiting 2 second. . . .'], [] 
		
	def on_connect(self, client, userdata, flags, rc):
		client.subscribe(self.topic)

	def on_message(self, client, userdata, message):
		#print("message topic=",message.topic)
		#print("message qos=",message.qos)
		img = base64.decodebytes(message.payload)
		self.payload = img
		self.img_received = True


################################################################
class WebCam(VideoBase):
	def __init__(self):
		super().__init__() 
		self.Class = "2"
		self.webcam = None
		self.file_name = "media/demo2.jpg"
		self.file_output = "media/output.jpg"
		self.showbox = False
		self.current = 0
		self.c_capture = True
	   
	def disconnect(self):
		self.webcam.release() 
		self.webcam = None
		self.con = False
	def stream(self):
		if self.con == False:
			file_name = "media/background.png"
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
		else:
			self.webcam = cv2.VideoCapture(0) 
			while True:
				
				if self.showbox == True:
					yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_output, 'rb').read() + b'\r\n')
					if time.time() - self.current > 2:
						self.showbox = False
						self.current = 0
						self.c_capture = True
				else:
					ret, frame = self.webcam.read()

					if not ret:
						print("Error: failed to capture image")
						break
					cv2.imwrite(self.file_name, frame)
					yield (b'--frame\r\n'
						b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_name, 'rb').read() + b'\r\n')


	def capture(self):
		if self.c_capture:
			self.c_capture = False
			name, box= face_ai(self.file_name) 
			self.note("get get get")
			self.updateAuthentication("20183651")
			if len(name)!=0:
				self.showbox = True
				self.current = time.time()
			else:
				name.append("Unknown")
				self.c_capture = True
			return name, box
		else:
			return ['Waiting 2 second. . . .'], [] 