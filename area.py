import sys
import time
import cv2
import configparser
import os
import win32ui


def on_EVENT_BUTTONDOWN(event, x, y, flags, userdata):
    global i, img, mydict, j, copy_img, cache, label
    if j > 4:
        if os.path.exists("plot/Annotation_file"):
            outFile = BASE_DIR + '/Annotation_file/'
        else:
            os.mkdir("plot/Annotation_file")
            outFile = BASE_DIR + '/Annotation_file/'
        filename_new = filename.split('.')[0] + "_finish" + '.' + filename.split(".")[1]
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
        elif j == 4:
            label = 'roi'
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
            elif j == 4:
                cv2.line(img, mydict[name[j]][i], mydict[name[j]][i + 1], (255, 0, 255), thickness=2,
                         lineType=cv2.LINE_AA)
            i += 1
            cv2.imshow("Label coordinates", img)
        print("[{},{}]".format(a[-1], b[-1]))  # 输出最后一次点击的坐标
        # 图片覆盖
    elif event == cv2.EVENT_MBUTTONDOWN:
        mydict[name[j]].clear()
        if j == 0:
            img = cache.copy()
        else:
            img = copy_img.copy()
        i = 0
        cv2.imshow('Label coordinates', img)
        print('-----------------撤销未封闭的坐标区域-------------------')
        # 右击将初始坐标与最终坐标相连，并保存内容
    elif event == cv2.EVENT_RBUTTONDOWN:
        if j == 0:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (0, 0, 255), thickness=4, lineType=cv2.LINE_AA)
        if j == 1:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (255, 0, 0), thickness=4, lineType=cv2.LINE_AA)
        if j == 2:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (238, 130, 238), thickness=4, lineType=cv2.LINE_AA)
        if j == 3:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (0, 255, 255), thickness=4, lineType=cv2.LINE_AA)
        if j == 4:
            cv2.line(img, mydict[name[j]][-1], mydict[name[j]][0], (255, 0, 255), thickness=4, lineType=cv2.LINE_AA)
        cv2.imshow("Label coordinates", img)
        copy_img = img.copy()
        conf = configparser.ConfigParser()
        conf.read(os.path.join(BASE_DIR, "plot/Localconfig.ini"), encoding='utf-8')
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
        elif j == 4:
            print(head + '-------------------roi区域---------------------')
        # conf.set(sections[0], head, ','.join(str(k) for k in mydict[name[j]]))
        # conf.write(open(os.path.join(BASE_DIR, "Localconfig.ini"), "w+", encoding='utf-8'))
        if head in options:
            print('---------------------修改坐标-------------------------------')
            # 文件读取的修改方式，但replace方法不适用于多内容替换
            # value = conf.get(sections[0], head)
            # file = open(r"Localconfig1.ini", "r+")
            # data = file.read()
            # file.seek(0)  # seek() 方法用于移动文件读取指针到指定位置。0是从文件开头
            # if value in data:
            #     data = data.replace(name + '=' + value, name + '=' + ','.join(str(i) for i in mydict[name[j]]))
            #     file.write(data)
            # configparser的修改文件内容
            # if j == 0:
            #     conf.set(sections[0], head, ','.join(str(k) for k in mydict[name[j]]))
            #     conf.write(open(os.path.join(BASE_DIR, "Localconfig.ini"), "w+", encoding='utf-8'))
            # else:
            conf.set(sections[0], head, ','.join(str(k) for k in mydict[name[j]]))
            conf.write(open(os.path.join(BASE_DIR, "plot/Localconfig.ini"), "w+", encoding='utf-8'))
        else:
            print('---------------------添加坐标-------------------------------')
            # file = open(os.path.join(BASE_DIR, "Localconfig.ini"), "a+", encoding='utf-8')
            # file.write("\n" + head + "=" + ','.join(str(k) for k in mydict[name[j]]))
            # file.close()
            with open(os.path.join(BASE_DIR, "plot/Localconfig.ini"), "a+", encoding='utf-8') as file:
                if j == 0:
                    file.write("\n\n" + head + "=" + ','.join(str(k) for k in mydict[name[j]]))
                else:
                    file.write("\n" + head + "=" + ','.join(str(k) for k in mydict[name[j]]))
        i = 0
        j += 1


if __name__ == '__main__':
    while True:
        # 表示打开文件对话框
        dlg = win32ui.CreateFileDialog(1)
        # 设置同级目录 windows下的设置方法
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        '''获取当前运行脚本的路径'''
        # 第一种方式 主要区分linux系统和windows系统
        # if getattr(sys, 'frozen', False):
        #     BASE_DIR = os.path.dirname(sys.executable)
        # else:
        #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # 第二种方式：解决临时目录的问题
        BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        if os.path.exists('plot/Localconfig.ini'):
            # file = open(os.path.join(BASE_DIR, "Localconfig.ini"), "a+", encoding='utf-8')
            # pass
            print('-------------------------读取文件------------------')
        else:
            print('-------------------------创建文件------------------')
            with open(os.path.join(BASE_DIR, "plot/Localconfig.ini"), "w", encoding='utf-8') as file_create:
                file_create.write('[location]')
        # 设置打开文件对话框中的初始显示目录
        dlg.SetOFNInitialDir(os.path.join(BASE_DIR, "photos"))
        dlg.DoModal()
        filePathname = dlg.GetPathName()  # 获取选择的文件名称
        filename = os.path.basename(filePathname)  # 带后缀的文件名
        split = filename.split('.')[0]  # 不带后缀的文件名
        img = cv2.imread(filePathname)  # 读取图片
        cache = img.copy()
        global copy_img
        a = []
        b = []
        i = 0
        j = 0
        name = ['list_pts_red', 'list_pts_blue', 'area_poly', 'people_area_poly', 'roi']
        mydict = {name[0]: [], name[1]: [], name[2]: [], name[3]: [], name[4]: []}
        cv2.namedWindow("Label coordinates", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Label coordinates", on_EVENT_BUTTONDOWN)
        cv2.imshow("Label coordinates", img)
        try:
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
        except AssertionError:
            cv2.destroyAllWindows()
            break
    cv2.waitKey()
    cv2.destroyAllWindows()
