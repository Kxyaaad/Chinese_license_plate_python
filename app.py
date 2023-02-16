import flask
import detect_plate
import json

app = flask.Flask(__name__)


@app.route('/test', methods=['post', 'get'])
def hello_world():
    imageUrl = flask.request.values.get('imageUrl')
    re = detect_plate.detect_image(imageUrl)
    if len(re) > 0:
        msg = ""
        if re[0]["detect_conf"] < 0.7:
            msg = "车牌区域可信度低"
        for conf in re[0]["rec_conf"]:
            if conf < 0.7:
                msg = "车牌号可信度低"
                break
        result = {"code": 200, "data": {}, "message": msg}
        result["data"]["plate_no"] = re[0]["plate_no"]
        result["data"]["plate_color"] = re[0]["plate_color"]
        result["data"]["plate_type"] = re[0]["plate_type"]
        color = result["data"]["plate_color"]
        car_type = 6
        car_number = re[0]["plate_no"]
        if color == "蓝色" or color == "白色" or color == "黑色":
            if "警" in car_number or "使" in car_number or "领" in car_number:
                car_type = 23
            else:
                car_type = 6
        elif color == "黄色":
            if len(result["data"]["plate_no"]) == 8:
                car_type = 19
            elif result["data"]["plate_type"] == 0:
                if "学" in result["data"]["plate_no"]:
                    car_type = 6
                else:
                    car_type = 5
            else:
                car_type = 8
        elif color == "绿色" or color == "黄绿色":
            if len(result["data"]["plate_no"]) == 8:
                car_type = 19
            else:
                car_type = 6
        result["data"]["car_type"] = car_type
        result = json.dumps(result, ensure_ascii=False)
        return result.__str__()
    else:
        result = {"code": 400, "data": None}
        result = json.dumps(result, ensure_ascii=False)
        return result


if __name__ == '__main__':
    app.run(port=8888, debug=False, host='127.0.0.1')
