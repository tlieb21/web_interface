#!/usr/bin/env python
import rospy
import cv2
from threading import Thread, Event
from flask import Flask, render_template, Response
import signal, sys
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

frame = None
bridge = CvBridge()
event = Event()
angle = 0

def on_image(msg):
    global frame
    cv_image = cv2.flip(cv2.flip(bridge.imgmsg_to_cv2(msg, desired_encoding = "passthrough"),0),1)
    #cv_image = cv2.rotate(bridge.imgmsg_to_cv2(msg, desired_encoding = "passthrough"), cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.imencode(".jpg",cv_image)[1].tobytes()
    event.set()

Thread(target=lambda: rospy.init_node('cam_listener', disable_signals=True)).start()
rospy.Subscriber("/camera/image_raw",Image, on_image)

app = Flask(__name__)

def get_frame():
    event.wait()
    event.clear()
    return frame

@app.route('/')
def index():
    angle = 180;
    return render_template('index.html', rotate=angle)

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/rot_left")
def rot_left():
    global angle
    if angle == 270:
        angle = 0
    else:
        angle = angle + 90
    return render_template('index.html', rotate=angle)

@app.route("/rot_right")
def rot_right():
    global angle
    if angle == 0:
        angle = 270
    else:
        angle = angle - 90
    return render_template('index.html', rotate=angle)
    

def signal_handler(signal, frame):
    rospy.signal_shutdown("end")
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)

