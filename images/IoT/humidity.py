import Adafruit_DH
sensor = Adafruit_DHT.DHT11
# Example using a Raspberry Pi with DHT sensor
# connected to GPIO4.
pin = 4
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
