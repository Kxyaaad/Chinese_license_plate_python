import warnings
import torch
import numpy as np
import torch.nn as nn
from torchvision import transforms
from plate_recognition.plateNet import MyNet_color
from PIL import Image
import extcolors

import cv2


# import extc

class MyNet(nn.Module):
    def __init__(self, class_num=6):
        super(MyNet, self).__init__()
        self.class_num = class_num
        self.backbone = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=(5, 5), stride=(1, 1)),  # 0
            torch.nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            nn.Dropout(0),
            nn.Flatten(),
            nn.Linear(480, 64),
            nn.Dropout(0),
            nn.ReLU(),
            nn.Linear(64, class_num),
            nn.Dropout(0),
            nn.Softmax(1)
        )

    def forward(self, x):
        logits = self.backbone(x)

        return logits


def init_color_model(model_path, device):
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print("color_rec_device:", device)
    # PATH = 'E:\study\plate\Chinese_license_plate_detection_recognition-main\weights\color_classify.pth'  # 定义模型路径
    class_num = 6
    warnings.filterwarnings('ignore')
    net = MyNet_color(class_num)
    net.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    net.eval().to(device)
    modelc = net

    return modelc


def plate_color_rec(img, model, device):
    originImage = img
    class_name = ['黑色', '蓝色', '', '绿色', '白色', '黄色']
    data_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = cv2.resize(data_input, (34, 9))
    image = np.transpose(image, (2, 0, 1))
    img = image / 255
    img = torch.tensor(img)
    normalize = transforms.Normalize(mean=[0.4243, 0.4947, 0.434],
                                     std=[0.2569, 0.2478, 0.2174])
    img = normalize(img)
    img = torch.unsqueeze(img, dim=0).to(device).float()
    xx = model(img)
    color = class_name[int(torch.argmax(xx, dim=1)[0])]
    if color == "绿色":  # 如果是绿色的，再检验是不是黄绿色
        img = cv2.cvtColor(originImage, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        colors_x = extcolors.extract_from_image(image, tolerance=20, limit=3)
        for colorArr in colors_x[0]:
            colorItem = colorArr[0]
            red = colorItem[0]
            green = colorItem[1]
            blue = colorItem[2]
            rgbColor = np.uint8([[[blue, green, red]]])
            hsv = cv2.cvtColor(rgbColor, cv2.COLOR_BGR2HSV)
            if 17 <= hsv[0][0][0] < 30 and 50 < hsv[0][0][1] <= 255 and 70 < hsv[0][0][
                2] <= 255:  # 黄色的HSV阈值 26-34, 橙色11 - 25
                return "黄绿色"
        return color
    return color


if __name__ == '__main__':
    class_name = ['black', 'blue', 'danger', 'green', 'white', 'yellow']
    data_input = cv2.imread("/mnt/Gpan/Mydata/pytorchPorject/myCrnnPlate/images/test.jpg")  # (高，宽，通道(B，G，R)),（H,W,C）
    device = torch.device("cuda" if torch.cuda.is_available else "cpu")
    model = init_color_model(
        "/mnt/Gpan/Mydata/pytorchPorject/Chinese_license_plate_detection_recognition/weights/color_classify.pth",
        device)
    color_code = plate_color_rec(data_input, model, device)
    print(color_code)
    print(class_name[color_code])
