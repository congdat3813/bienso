"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import base64
from PIL import Image
from io import BytesIO
import socketio
import base64
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
sio = socketio.Server()
application = socketio.WSGIApp(sio, application)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
@sio.on("img_jpg")
def receiveImg(sid, data):
    img = base64.b64decode(data)
    im = Image.open(BytesIO(img))
    im.save('polls/static/image/image1.jpeg', 'JPEG')
    