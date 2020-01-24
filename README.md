# web_interface

Web server to stream video from a ros topic. Working to allow drawing/ markup on the video stream

## Usage:
`roslaunch video_stream_opencv camera.launch video_stream_provider:=<x>`
* Replace `<x>` by the number of the video feed to open /dev/videox 

`gunicorn --threads 5 --workers 1 --bind <your_ip>:8080 app:app`
* Replace `<your_ip>` by the machine's ip.

## Prerequisites:
Flask, Ros, Gunicorn

