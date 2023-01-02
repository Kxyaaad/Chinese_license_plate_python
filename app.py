import flask
import detect_plate
app = flask.Flask(__name__)
@app.route('/test', methods=['post'])
def hello_world():
    imageUrl = flask.request.values.get('imageUrl')
    re = detect_plate.detect_image(imageUrl)
    return re[0]["plate_no"].__str__()
if __name__ == '__main__':
    app.run(port=8888,debug=True,host='127.0.0.1')