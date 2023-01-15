import flask
import detect_plate
import json

app = flask.Flask(__name__)


@app.route('/test', methods=['post', 'get'])
def hello_world():
    imageUrl = flask.request.values.get('imageUrl')
    re = detect_plate.detect_image(imageUrl)
    if len(re) > 0:
        result = {"code": 200, "data": {}}
        result["data"]["plate_no"] = re[0]["plate_no"]
        result["data"]["plate_color"] = re[0]["plate_color"]
        result["data"]["plate_type"] = re[0]["plate_type"]
        result = json.dumps(result, ensure_ascii=False)

        return result.__str__()
    else:
        result = {"code": 400, "data": None}
        result = json.dumps(result, ensure_ascii=False)
        return result


if __name__ == '__main__':
    app.run(port=8888, debug=False, host='127.0.0.1')
