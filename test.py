# coding:utf-8
import os
import platform
import pyautogui
import time
import cv2 as cv
import numpy as np
import traceback
import configparser
import ast
from PIL import ImageGrab, ImageDraw, ImageFont, Image
from termcolor import colored
from colorama import init
init()

PROJ_DIR = os.getcwd()
CONF_DIR = os.path.join(PROJ_DIR,'src','conf')
PIC_DIR = os.path.join(PROJ_DIR,'src','pics')
SCREEN_DIR = os.path.join(PROJ_DIR,'screenshots')

now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
setting = 'DEFAULT'

redprint = lambda x: print(colored(x,'red'))
greenprint = lambda x: print(colored(x,'green'))
blueprint = lambda x: print(colored(x,'blue'))

# 加载配置文件
conf = configparser.ConfigParser()
try:
    with open(os.path.join(CONF_DIR,'setting.cfg'),'r') as f:
        conf.read_file(f)
        rec_func = conf[setting]['rec_func']
        print(rec_func)
except Exception as e:
    error_info = traceback.format_exc()
    redprint(f'Error:{error_info}')
    exit()

# 用于简化识别图片的函数（综合）
def recog_img(base_img,recog_img):
    # 预处理要查找的基础图片（大图）
    try:
        if type(base_img) == Image.Image:
            # PIL to numpy
            base_img = cv.cvtColor(np.asarray(base_img), cv.COLOR_RGB2BGR)
        else:
            base_img = cv.imread(base_img)
    except Exception as e:
        error_info = traceback.format_exc()
        redprint(f'Error:{error_info}')
        exit()
    # 加载预识别图片（小图）
    pre_recog = cv.imread(recog_img)
    # cv模块进行识别 匹配方式：TM_CCOEFF_NORMED
    match_loc = cv.matchTemplate(base_img,pre_recog,rec_func)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(match_loc)
    pre_recog_center = (pre_recog.shape[1]//2 + max_loc[0],pre_recog.shape[0]//2 + max_loc[1])
    result = pre_recog_center
    return result

if __name__ == '__main__':
    blueprint('Starting...')
    greenprint(f'Current working directory:{PROJ_DIR}')
    print(colored(PROJ_DIR,'blue'))
    print(colored(CONF_DIR,'blue'))
    print(colored(PIC_DIR,'blue'))
    print(colored(SCREEN_DIR,'blue'))

    # 获取屏幕截图
    screen_shot = ImageGrab.grab()
    # print('screen:',type(screen_shot))
    # PIL to numpy

    # 由于截图使用PIL库，所以需要转换为cv2格式
    preload_screen = cv.cvtColor(np.asarray(screen_shot), cv.COLOR_RGB2BGR)
    # 加载预识别图片
    pre_recog = cv.imread(os.path.join(PIC_DIR,'notepad_ico.png'))
    # print('recog',type(pre_recog))
    print('Screen Size:',preload_screen.shape)

    # 预识别匹配 匹配方式：TM_CCOEFF_NORMED
    match_loc = cv.matchTemplate(preload_screen,pre_recog,cv.TM_CCOEFF_NORMED)
    print(cv.minMaxLoc(match_loc))
    # 根据识别结果获取坐标点
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(match_loc)
    # print(match_loc)

    # 计算中心点（点击位置）
    print(min_loc,max_loc)
    print(pre_recog.shape,preload_screen.shape[0]/2,preload_screen.shape[1]/2)
    pre_recog_center = (pre_recog.shape[1]//2 + max_loc[0],pre_recog.shape[0]//2 + max_loc[1])
    # 绘制结果
    cv.rectangle(preload_screen,max_loc,(max_loc[0]+pre_recog.shape[1],max_loc[1]+pre_recog.shape[0]),(0,0,255),2)
    cv.circle(preload_screen,max_loc,3,(0,255,0),-1)
    cv.circle(preload_screen,pre_recog_center,3,(0,255,255),-1)
    cv.putText(preload_screen,'loc:'+str(max_loc) + 'center:' + str(pre_recog_center),max_loc,cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
    # 点击焦点至Notepad 并输入文字
    pyautogui.click(pre_recog_center)
    # for i in range(100):
    #     pyautogui.press('backspace')
    pyautogui.press('enter')
    pyautogui.typewrite('auto input'+str(now)+str(pre_recog_center),interval=0.05)
    # cv.imshow('screen',preload_screen)
    
    greenprint('finished')
    # cv.waitKey(0)


# screen_shot = pyautogui.screenshot()
# ico_loc = pyautogui.locateOnScreen(os.path.join(PIC_DIR,'notepad_ico.png'))
# print(ico_loc)
# screen_shot.show()
# screen_shot.save(SCREEN_DIR + f'/test{now}.png')

