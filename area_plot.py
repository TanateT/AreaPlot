import configparser
import os
import sys
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory

"""
1.生成exe文件无压缩版
pyinstaller -F -w -i Sugar-coated_haws.png plot_area.py 
2.生成exe文件压缩版
pyinstaller -F -w -i Sugar-coated_haws.png area_plot.py 
--upx-dir C:/mython/projects/torchlearning/opencv/area/upx/upx-3.96-win64
3.nuitka打包
--windows-disable-console
nuitka --standalone --mingw64 --show-progress  --show-memory --nofollow-import-to=urllib3,opencv-python,PIL,numpy,configparser,http,email --plugin-enable=tk-inter   --output-dir=out --windows-icon-from-ico=Sugar-coated_haws.png area_plot.py
nuitka --standalone --mingw64 --show-memory --show-progress --nofollow-imports --plugin-enable=tk-inter --follow-import-to=urllib3,cv2,PIL,http,email,cffi,numpy,configparser --output-dir=out  area_plot.py

"""


# 翻页功能设置
def change_photos(next_no):
    global current_photo_no
    current_photo_no += next_no
    if current_photo_no > len(photos) - 1:
        current_photo_no = 0
    elif current_photo_no < 0:
        current_photo_no = len(photos) - 1
    number_var.set("{}/{}   图片名:{}".format(current_photo_no + 1, len(photos), photos_list[current_photo_no]))
    photo_label.configure(image=photos[current_photo_no])


# 图片标注
def on_EVENT(event, x, y, flags, userdata):
    global i, img, mydict, j, copy_img, cache, label, filename, a, b
    # 保存文件
    if j > 3:
        if os.path.exists("Annotation_file"):
            outFile = BASE_DIR + '/Annotation_file/'
        else:
            os.mkdir("Annotation_file")
            outFile = BASE_DIR + '/Annotation_file/'
        # 获取文件后缀名
        suffix_filename = filename.split('.')[-1]
        # 获取新的文件名
        filename_new = filename.split('.' + suffix_filename)[0] + "_finish" + '.' + suffix_filename
        cv2.imwrite(outFile + str(filename_new), img)
        time.sleep(1)
        print('------------------------内容更新成功-------------------------')
        cv2.destroyAllWindows()

    # 左击获取点的坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "[%d,%d]" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 3, (255, 0, 0), thickness=-1)
        if j == 0:
            label = 'Red'
        elif j == 1:
            label = 'Blue'
        elif j == 2:
            label = 'Car'
        elif j == 3:
            label = 'People'
        # elif j == 4:
        #     label = 'Roi'
        cv2.putText(img, xy + f'{label}', (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), thickness=2)
        mylist = [x, y]
        mydict[name[j]].append(mylist)
        if len(mydict[name[j]]) >= 2:
            if j == 0:
                cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (0, 0, 255), thickness=2,
                         lineType=cv2.LINE_AA)
            elif j == 1:
                cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (255, 0, 0), thickness=2,
                         lineType=cv2.LINE_AA)
            elif j == 2:
                cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (238, 130, 238), thickness=2,
                         lineType=cv2.LINE_AA)
            elif j == 3:
                cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (0, 255, 255), thickness=2,
                         lineType=cv2.LINE_AA)
            # elif j == 4:
            #     cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (255, 0, 255), thickness=2,
            #              lineType=cv2.LINE_AA)
            i += 1
            cv2.imshow("Label coordinates", img)
        print("[{},{}]".format(a[-1], b[-1]))  # 输出最后一次点击的坐标

    # 鼠标中间按钮点击撤销之前不合适的标注
    elif event == cv2.EVENT_MBUTTONDOWN:
        mydict[name[j]].clear()
        if j == 0:
            img = cache.copy()
        else:
            img = copy_img.copy()
        i = 0
        cv2.imshow('Label coordinates', img)
        print('-----------------撤销未封闭的坐标区域-------------------')

    # 鼠标右击将初始坐标与最终坐标相连，并保存内容
    elif event == cv2.EVENT_RBUTTONDOWN:
        if j == 0:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (0, 0, 255), thickness=4, lineType=cv2.LINE_AA)
        if j == 1:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (255, 0, 0), thickness=4, lineType=cv2.LINE_AA)
        if j == 2:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (238, 130, 238), thickness=4, lineType=cv2.LINE_AA)
        if j == 3:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (0, 255, 255), thickness=4, lineType=cv2.LINE_AA)
        # if j == 4:
        #     cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (255, 0, 255), thickness=4, lineType=cv2.LINE_AA)
        cv2.imshow("Label coordinates", img)
        copy_img = img.copy()
        # 读取.ini文件
        conf = configparser.ConfigParser()
        conf.read(os.path.join(BASE_DIR, "Localconfig.ini"), encoding='utf-8')
        sections = conf.sections()
        options = conf.options(sections[0])
        head = name[j] + str(split)
        if j == 0:
            print(head + '------------------红色检测区域-------------------')
        elif j == 1:
            print(head + '------------------蓝色检测区域-------------------')
        elif j == 2:
            print(head + '------------------车检测区域---------------------')
        elif j == 3:
            print(head + '------------------人检测区域---------------------')
        # elif j == 4:
        #     print(head + '-------------------roi区域---------------------')
        if head in options:
            print('---------------------修改坐标-------------------------------')
            conf.set(sections[0], head, ','.join(str(k) for k in mydict[name[j]]))
            conf.write(open(os.path.join(BASE_DIR, "Localconfig.ini"), "w+", encoding='utf-8'))
        else:
            print('---------------------添加坐标-------------------------------')
            with open(os.path.join(BASE_DIR, "Localconfig.ini"), "a+", encoding='utf-8') as file:
                if j == 0:
                    file.write("\n\n" + head + " = " + ','.join(str(k) for k in mydict[name[j]]))
                else:
                    file.write("\n" + head + " = " + ','.join(str(k) for k in mydict[name[j]]))
        i = 0
        j += 1


def label_coord():
    global split, cache, a, b, i, j, mydict, name, filename, copy_img, img

    if os.path.exists('Localconfig.ini'):
        print('-------------------------读取文件------------------')
    else:
        print('-------------------------创建文件------------------')
        with open(os.path.join(BASE_DIR, "Localconfig.ini"), "w", encoding='utf-8') as file_create:
            file_create.write('[location]')

    # 获取选择的文件名称
    filePathname = photos_path[current_photo_no]
    # 带后缀的文件名
    filename = os.path.basename(filePathname)
    # 不带后缀的文件名
    split = filename.split('.')[0]
    # 读取图片
    img = cv2.imread(filePathname)
    # 图片复制用于覆盖撤销功能
    cache = img.copy()

    # 变量定义
    a = []
    b = []
    i = 0
    j = 0
    # 对应的画框的类别名
    name = ['list_pts_red', 'list_pts_blue', 'area_poly', 'people_area_poly', 'roi']
    mydict = {name[0]: [], name[1]: [], name[2]: [], name[3]: [], name[4]: []}

    # opencv设置图片读取窗口
    cv2.namedWindow("Label coordinates", cv2.WINDOW_NORMAL)
    # opencv设置鼠标按键函数
    cv2.setMouseCallback("Label coordinates", on_EVENT)
    cv2.imshow("Label coordinates", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def close_window():
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("960x700+100+100")
    root.title('图片编辑器')
    # tkinter 获取目录
    IMG_PATH = askdirectory()

    # 定位当前目录
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    # 图片读取类别设置
    image_format = ['bmp', 'jpg', 'png', 'jpeg', 'gif', 'psd']

    # 获取文件
    photos_list = [i for i in os.listdir(IMG_PATH) if i.split(".")[-1] in image_format]

    # 获取图片地址列表
    photos_path = [os.path.join(IMG_PATH, photo) for photo in photos_list]

    # PIL读取图片
    photos = [ImageTk.PhotoImage(Image.open(photo)) for photo in photos_path]
    time.sleep(1)
    current_photo_no = 0
    photo_label = tk.Label(root, image=photos[current_photo_no], width=960, height=640)
    photo_label.pack()
    number_var = tk.StringVar()
    number_var.set("1/{}    图片名:{}".format(len(photos), photos_list[current_photo_no]))
    tk.Label(root, textvariable=number_var, bd=1, relief=tk.SUNKEN, anchor=tk.CENTER).pack(fill=tk.X)
    button_frame = tk.Frame(root)
    button_frame.pack()

    # 按键设置
    quit_ = tk.Button(button_frame, text="退出")
    prev_photo = tk.Button(button_frame, text="上一页")
    next_photo = tk.Button(button_frame, text="下一页")
    image_coord = tk.Button(button_frame, text="图像像素点标注")

    # 按键位置
    quit_.pack(side=tk.LEFT, anchor=tk.CENTER)
    prev_photo.pack(side=tk.LEFT, anchor=tk.CENTER)
    next_photo.pack(side=tk.LEFT, anchor=tk.CENTER)
    image_coord.pack(side=tk.LEFT, anchor=tk.E)

    # 按键函数设置
    quit_.config(command=lambda: close_window())
    prev_photo.config(command=lambda: change_photos(-1))
    next_photo.config(command=lambda: change_photos(1))
    image_coord.config(command=lambda: label_coord())

    root.mainloop()
