# 最邻近差值位于Week2.py文件第21至44行
# 双线性插值位于Week2.py文件第46至80行
from PIL import Image
import numpy as np
import cv2 as cv2
import fire

if __name__ == '__main__':
    fire.Fire()  # 使用命令行参数

def cv_file(pix_array_out, file_out_path):
    img_out = Image.fromarray(np.uint8(pix_array_out))  # 生成新图片
    img_out.save(file_out_path)  # 保存图片
    # 读取图像
    picture = cv2.imread(file_out_path)
    # 显示图像
    cv2.imshow('Output', picture) 
    cv2.waitKey(0)

# 最邻近插值
def nearist():
    n = eval(input("请输入放大倍数："))
    name = input("请输入待放大图片名称：")
    # file_in = input('Please enter the name of Image(with type)')
    img_in = Image.open(name)
    img_out = Image.new(mode=img_in.mode,size=((img_in.size[0])*n,(img_in.size[1])*n))#放大n倍
    pix = img_in.load()
    width = img_in.size[0]
    height = img_in.size[1]
    rgb_out = []

    for i in range(height):
        for z in range(n):
            for j in range(width):
                r,g,b= pix[j,i]
                for k in range(n):
                    rgb_out.append((r,g,b))
                k = 0
            j = 0
        z = 0
    img_out.putdata(rgb_out)
    out_name = input("请输入保存路径：")
    img_out.save(out_name)
    

def bilinear(width_out, height_out, img_in):  # 双线性插值
    
    height_in = img_in.height         # 获得原始图片的高
    width_in = img_in.width           # 获得原始图片的宽
    img_array = np.array(img_in)       # 读取原始图片并将其像素点保存为一个3维数组
    height_t1 = height_in / height_out
    height_t2 = (height_in - 1) / height_out
    width_t1 = width_in / width_out
    width_t2 = (width_in - 1) / width_out
    # 计算插值，生成图片
    pix_out = list()
    row = list()
    for y in range(height_out):
        if height_t1 > 1:
            arr_y = (y + 0.5) * height_t1 - 0.5  # 下采样纵坐标变换
        else:
            arr_y = (y + 0.5) * height_t2 - 0.5  # 上采样纵坐标变换
        for v in range(width_out):
            if width_t1 > 1:
                arr_x = (v + 0.5) * width_t1 - 0.5  # 下采样横坐标变换
            else:
                arr_x = (v + 0.5) * width_t2 - 0.5  # 上采样横坐标变换
            v = arr_x % 1.0
            u = arr_y % 1.0
            i = int(arr_x)
            j = int(arr_y)
            arr_rgb = list()
            for k in range(3):  # 将RGB值依次保存成一个列表
                arr_rgb.append(round((1-v)*(1-u)*img_array[j][i][k]\
                                +(1-v)*u*img_array[min(j+1,width_in-1)][i][k]\
                                +v*(1-u)*img_array[j][min(i+1,height_in-1)][k]\
                                +v*u*img_array[min(j+1,width_in-1)][min(i+1,height_in-1)][k]))
            row.append(arr_rgb)  # 把RGB值依次保存至行列表中
        pix_out.append(row)  # 将每一行的元素保存为一个二维列表
    return pix_out

# 获取图像
x_image = Image.open('test.png')
image = x_image.convert('RGB') # 将图片转为RGB色彩模式
# 图像处理

algorithm = input("请输入生成图像的算法：（最邻近插值/双线性插值）:")
if algorithm not in ['最邻近插值', '双线性插值']:
    print("ERRROR!!")
else: 
    if algorithm == '最邻近插值':  # 最近邻插值
        nearist()
    
# 双线性插值        
    elif algorithm == '双线性插值':
        height = eval(input("请输入生成图片高度："))
        width = eval(input("请输入生成图片宽度："))
        path = input("请输入保存路径：")  
        arr_new = bilinear(width, height, image)
        cv_file(arr_new, path)