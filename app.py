from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Replace 'your_camera_ip' with the actual IP address of your OAK-D PoE camera
camera_ip = 'http://192.168.1.13/video'
camera = cv2.VideoCapture(camera_ip)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
