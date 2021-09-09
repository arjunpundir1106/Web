import os
from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime
import picamera
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import StringIO
from login import *

#initializing the camera
camera = picamera.PiCamera()

#--//-- GPIO initialization --//--
pin = 18
pin2 = 23

GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
GPIO.setwarnings(False)

GPIO.setup(pin,GPIO.IN)		#pin 1 set as input
GPIO.setup(pin2,GPIO.IN)	#pin 2 set as input


def send_email(message,path):
	try:
		fromaddr = from_address
		password = email_password
		toaddr = destination

		msg = MIMEMultipart()

		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "incoming telemetry"

		body = message

		msg.attach(MIMEText(body, 'plain'))
	
		attachment = open(path, "rb")
		part = MIMEBase("application", "octet-stream")
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header("Content-Disposition", "attachment;filename=image.jpg")
		#print(path)
		#part.add_header("Content-Disposition", "attachment; filename=path")
		msg.attach(part)

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr,password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()

	except:
		pass

# Start loop
while True:
	try:
		#image capture
		timestamp = str(datetime.now().strftime("%Y-%m-%d--%H:%M:%S"))
		#filename = timestamp+".jpg"
		#path = "snapshots/"+filename
		path = "image.jpg"
		camera.capture(path)

		#moisture measurement
		if (GPIO.input(pin) == True):
			message1 = "Plant 1: soil gets dry at "+timestamp+" :/"
			print('3.3V – Dry soil')
		else:
			print('0V – Moist soil')
			message1 = "Plant 1: soil is moist at "+timestamp+" :)"

		if (GPIO.input(pin2) == True):
			message2 = "Plant 2: soil gets dry at "+timestamp+" :/"
			print('3.3V – Dry soil')
		else:
			print('0V – Moist soil')
			message2 = "Plant 2: soil is moist at "+timestamp+" :)"
		message = message1+"\n"+message2
	except:
		pass

	send_email(message,path)
	sleep(7200);