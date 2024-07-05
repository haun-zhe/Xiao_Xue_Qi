# -*- coding: utf-8 -*-

'''
启动摄像头主程序

用法:
python startingcameraservice.py
python startingcameraservice.py --location room

直接执行即可启动摄像头，浏览器访问 http://192.168.1.156:5001/ 即可看到
摄像头实时画面

'''
import argparse
from flask import Flask, render_template, Response, request,jsonify

from util.facialutil import FaceUtil


from collectfaceinfo import Collectingfaces
from util.camerautil import VideoCamera
from startrecording import Startingrecording
from flask_cors import *
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from falltest import fall_main
from fencetest import fence_main

# 传入参数
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--location", required=False,
                default='room', help="")
args = vars(ap.parse_args())
location = args['location']

if location not in ['room', 'yard', 'corridor', 'desk']:
    raise ValueError('location must be one of room, yard, corridor or desk')

# API
app = Flask(__name__)

video_camera = None
global_frame = None
# 设置跨域
# CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')

@app.route('/')
def index():
    return render_template(location + '_camera.html')


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera == None:
        video_camera = VideoCamera()
        s = Startingrecording(location)
        s.startStartrecord()
        # video_camera=Collectingfaces("images","104")
        # video_camera.startCollect()

        # video_camera=Checkingfalldetection("../images/tests/videos/3.mp4")
        # video_camera.startfall()

        # video_camera=Checkingfence("../images/tests/videos/yard_01.mp4")
        # video_camera.startfence()

        # video_camera=Checkingstrangersandfacialexpression("")
        # video_camera=Checkingstrangersandfacialexpression()

        # video_camera.startstrangerFacial()
        # video_camera=Checkingvolunteeractivity("../images/tests/videos/desk_01.mp4")
        # video_camera.startactivity()

    status = request.form.get('status')
    save_video_path = request.form.get('save_video_path')

    if status == "true":
        video_camera.start_record(save_video_path)
        return 'start record'
    else:
        video_camera.stop_record()
        return 'stop record'


def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()
        s = Startingrecording("room")
        s.startStartrecord()
        video_camera=Collectingfaces("images","104")
        video_camera.startCollect()

        # video_camera=Checkingfalldetection("../images/tests/videos/3.mp4")
        # video_camera.startfall()

        # video_camera=Checkingfence("../images/tests/videos/yard_01.mp4")
        # video_camera.startfence()

        # video_camera=Checkingstrangersandfacialexpression("../images/tests/videos//room_01.mp4")
        # video_camera=Checkingstrangersandfacialexpression("")
        # video_camera.startstrangerFacial()

        # video_camera=Checkingvolunteeractivity("../images/tests/videos/desk_01.mp4")
        # video_camera.startactivity()

    while True:

        frame = video_camera.get_frame()
        if frame is not None:
            if frame != global_frame:
                global_frame = frame
                # print("上传一帧")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame
                       + b'\r\n\r\n')
        elif global_frame != None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + global_frame + b'\r\n\r\n')


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/fall_rec')
def fall_rec():
    fall_main()
    return "监控结束"

@app.route('/check_fence')
def check_fence():
    fence_main()
    return "监控结束"

def recognize_face(image):
    print("开始识别")
    faceutil = FaceUtil('./models_saving/face_recognition_hog.pickle')
    face_location_list,names = faceutil.get_face_location_and_name(image)
    print(face_location_list,names)
    return bool(face_location_list)  # 或者 False，根据实际情况

@app.route('/face_rec', methods=['POST'])
def face_rec():
    try:
        data = request.get_json()
        photo = data['photo']
        print('Received photo')

        # 解码图像
        image_data = base64.b64decode(photo.split(',')[1])  # 去掉base64头部信息
        image = Image.open(BytesIO(image_data))
        image = np.array(image)

        # 保存图像到本地
        image_pil = Image.fromarray(image)
        image_pil.save("received_image.png")
        print('Image saved successfully')

        # 调用人脸识别函数
        result = recognize_face(image)

        if result:
            response = {
                'code': 200,
                'message': '登陆成功，欢迎您'
            }
        else:
            response = {
                'code': 400,
                # 'message': '人脸登陆失败'
            }

    except Exception as e:
        response = {
            'code': 500,
            'message': f'内部服务器错误: {str(e)}'
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True, port=5001)

