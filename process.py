from pathlib import Path
import os
import numpy as np
import torch
# from unet import unet
from typing import Dict


import json
from segmentation import MySegmentation
import SimpleITK
from PIL import Image
import numpy as np

# count           = False
# name_classes    = ["background", "head", "SP"]

execute_in_docker = True
# path = "C:\\Users\\lalala\\Desktop\\Unetvgg\\VOCdevkit\\VOC2007\\JPEGImages"

class Nodule_seg:
    def __init__(self):
        self.input_dir = Path("/input/images/pelvic-2d-ultrasound/") if execute_in_docker else Path("./test/")
        # self.input_dir = Path("/input/images/pelvic-2d-ultrasound/") if execute_in_docker else Path(path)
        self.output_dir = Path("/output/images/symphysis-segmentation/") if execute_in_docker else Path("./output/")
        # todo Load the trained model
        if execute_in_docker:
            path_model = "/opt/algorithm/model_weights/best_model.pth"
        else:
            path_model = "model_weights/best_model.pth"
        self.md = MySegmentation(path_model=path_model)
        load_success = self.md.load_model()
        if load_success:
            print("Successfully loaded model.")

    def load_image(self, image_path) -> SimpleITK.Image:
        image = SimpleITK.ReadImage(str(image_path))  # 读取mha格式图像
        return image

    def predict(self, input_image: SimpleITK.Image):
        # 获取输入图片，其为numpy形式
        image_data = SimpleITK.GetArrayFromImage(input_image)  # 将读取的mha图像转换为numpy数组

        # 预测分割图像
        pred = self.md.process_image(image_data)
        # 处理并储存分割结果，pred为Image格式
            
        pred = SimpleITK.GetImageFromArray(np.asarray(pred)) # 转为mha格式
        return pred

    def write_outputs(self, image_name, outputs):
        if not os.path.exists('/output/images/symphysis-segmentation'):
            os.makedirs('/output/images/symphysis-segmentation')
        SimpleITK.WriteImage(outputs, '/output/images/symphysis-segmentation/'+ image_name +'.mha')
        # outputs.save(os.path.join('/output/images/symphysis-segmentation/' + image_name + '.png'))

    def process(self):
        image_paths = list(self.input_dir.glob("*.mha"))
        for image_path in image_paths:
            image_name = os.path.basename(image_path).split('.')[0]
            image = self.load_image(image_path)
            result = self.predict(image)
            self.write_outputs(image_name, result)
        print("Success hsiadhfjowiqjeoijfosdj9832049820sahfdi389u4903u409")

if __name__ == "__main__":
    Nodule_seg().process()
