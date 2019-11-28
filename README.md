# RaspberryPi OCR Live

We can run live stream RaspberryPi and do OCR recognition. This also converts OCR to Speech using GTTS (Google's Text to Speech) module running on python.

For OCR purposes we can use either tesseract (offline) or ocr.space (online api). Online API gives better accuracy, hence we are using the same here.

## Modules
- Tesseract (offline)
- Requests (online)
- piCamera
- socketserver, http

## How to start 
- Go to terminal and connect to RaspberryPi via SSH

`
ssh pi@raspberrypi.local
`
- Run the python code for hosting the OCR server (port 8000)

`
python3 rpi_camera_surveillance_system.py
`
- To get the 'hoo.mp3' Text-To-Speech-File directly from server, we are doing this jugaad. We run another python server at different port 8888

`
python -m SimpleHTTPServer 8888
`

## Screenshots

<img src="https://github.com/geekykant/RaspberryPi_OCR_Live/blob/master/screens/image6.jpeg?raw=true"></th>

<table>
  <th>
<img height="50%" src="https://github.com/geekykant/RaspberryPi_OCR_Live/blob/master/screens/image2.jpeg?raw=true"></th>

<th>
<img height="50%" src="https://github.com/geekykant/RaspberryPi_OCR_Live/blob/master/screens/image4.jpeg?raw=true"></th>
</table>
