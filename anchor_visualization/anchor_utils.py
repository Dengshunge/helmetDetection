import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def GT_show():
    '''
    将GT框画在原图上,进行可视化.
    需要配置的两个参数是path与save_path,分别表示图片路径与保存路径
    注意,这里的图片与xml文件放在同一个文件夹下.
    '''
    path = "/home/data/20"
    save_path = "/project/train/src_repo/tmp_pic"
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('xml'):
                continue
            filename = file.split('.')[0]
            print(filename)
            img_path = os.path.join(root, file)
            xml_path = os.path.join(root, filename + '.xml')

            img = cv2.imread(img_path)
            target = ET.parse(xml_path).getroot()
            for obj in target.iter("object"):
                name = obj.find('name').text

                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
                cv2.putText(img, name, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # cv2.imshow("img", img)
            # cv2.waitKey()
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cv2.imwrite(os.path.join(save_path, file), img)


def get_height_width():
    '''
    统计原图的GT框的宽度与高度,进行可视化,注意,这里没有进行缩放
    '''
    path = "/home/data/20"
    savepath = "/project/train/src_repo/tmp_pic"
    HW_data = []
    for root, _, files in os.walk(path):
        for file in files:
            if not file.endswith('xml'):
                continue
            filename = file.split('.')[0]
            xml_path = os.path.join(root, filename + '.xml')

            target = ET.parse(xml_path).getroot()
            for obj in target.iter("object"):
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                W, H = xmax - xmin + 1, ymax - ymin + 1
                HW_data.append([W, H])
    HW_data = np.array(HW_data)
    plt.scatter(HW_data[:, 0], HW_data[:, 1], s=1)
    plt.xlabel("Width")
    plt.ylabel("Height")
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    plt.savefig(os.path.join(savepath, "Width_Height.jpg"), dpi=600)


if __name__ == '__main__':
    # GT_show()
    get_height_width()
