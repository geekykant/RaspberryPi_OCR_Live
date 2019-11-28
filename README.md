# RaspberryPi OCR Live

We can run live stream RaspberryPi and do OCR recognition. This also converts OCR to Speech using GTTS (Google's Text to Speech) module running on python.

For OCR purposes we can use either tesseract (offline) or ocr.space (online api). Online API gives better accuracy, hence we are using the same here.

## Modules
- Tesseract (offline)
- Requests (online)
- piCamera
- socketserver, http
