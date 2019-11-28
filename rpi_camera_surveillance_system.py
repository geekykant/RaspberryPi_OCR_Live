# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import requests

camera = picamera.PiCamera(resolution='640x480', framerate=30)

print("OCR Server Started....")

PAGE="""\
<html style="font-family: Arial;">
<head>
<title>Raspberry Pi - Live OCR Camera</title>
</head>
<body>
<center><h1 style="color: blue;"> Raspberry Pi - OCR Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>

<form action="/do_ocr" method="get" id="form1">
</form>

<button type="submit" style="font-size: 24px;left: 50%;position: relative;color: white;background:blue" form="form1" value="Submit" id="btn">Submit</button>

</body>

</html>
"""

PAGE_1="""\
<html style="font-family: Arial;">
<head>
<title>Raspberry Pi - Live OCR Camera</title>
</head>
<body>
<center><h1 style="color: blue;"> Raspberry Pi - OCR Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>

<form action="/do_ocr" method="get" id="form1">
</form>

<button type="submit" style="font-size: 24px;left: 50%;position: relative;color: white;background:blue" form="form1" value="Submit" id="btn">Submit</button>

</body>

<center><h1>Text Detected: {text}</h1><center>

<div>
<audio controls autoplay>
  <source src="http://192.168.0.108:8888/ho.mp3" type="audio/mpeg">
Your browser does not support the audio element.
</audio>

</div>

</html>
"""

PAGE_2="""\
<html style="font-family: Arial;">
<head>
<title>Raspberry Pi - Live OCR Camera</title>
</head>
<body>
<center><h1 style="color: blue;"> Raspberry Pi - OCR Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>

<form action="/do_ocr" method="get" id="form1">
</form>

<button type="submit" style="font-size: 24px;left: 50%;position: relative;color: white;background:blue" form="form1" value="Submit" id="btn">Submit</button>

</body>

<center><h1>Text Detected: {text}</h1><center>

<div>

</div>

</html>
"""

from gtts import gTTS 

from PIL import Image
import pytesseract
import simplejson as json

language = 'en'
filename = 'image1.jpg'
payload = {'apikey': '27a5e79ce888957'}

def get_ocr_string():
    with open(filename,'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',files = {filename : f},data = payload)
        data = json.loads(r.text)
        return data['ParsedResults'][0]['ParsedText']

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path.startswith('/do_ocr'):
            camera.capture('image1.jpg')

            # img =Image.open ('image1.jpg')
            # ocr_text = pytesseract.image_to_string(img, config='')
            ocr_text = get_ocr_string()
            print("ocr value: " + ocr_text)

            if not ocr_text:
            	ocr_text = "Text not found!"
            	content = PAGE_2.format(text=ocr_text).encode('utf-8')

            else:
            	myobj = gTTS(text=ocr_text, lang=language, slow=False) 
            	myobj.save("ho.mp3") 
            	content = PAGE_1.format(text=ocr_text).encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        # elif self.path.startswith('/ho.mp3'):
        #     self.send_response(200) 
        #     music_mp3 = open('ho.mp3', 'rb')
        #     self.wfile.write(music_mp3)
        #     self.end_headers()
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

while(True):
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
