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
# 初始化路径
PROJ_DIR = os.getcwd()
CONF_DIR = os.path.join(PROJ_DIR,'src','conf')
PIC_DIR = os.path.join(PROJ_DIR,'src','pics')
SCREEN_DIR = os.path.join(PROJ_DIR,'screenshots')
# 初始化量
NOW = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
SETTING = 'DEFAULT'

# 定义打印颜色函数
redprint = lambda x: print(colored(x,'red'))
greenprint = lambda x: print(colored(x,'green'))
blueprint = lambda x: print(colored(x,'blue'))
blackprint = lambda x: print(colored(x,'black'))
whiteprint = lambda x: print(colored(x,'white'))

# 加载配置文件
conf = configparser.ConfigParser()
try:
    with open(os.path.join(CONF_DIR,'setting.cfg'),'r') as f:
        conf.read_file(f)
        rec_func = int(conf[SETTING]['rec_func'])
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

# 主函数
if __name__ == '__main__':
    blueprint('Starting...')
    timer_start = time.perf_counter()
    greenprint(f'Current working directory:{PROJ_DIR}')
    print(cv.cuda.getCudaEnabledDeviceCount())
    # 获取屏幕截图
    screen_shot = ImageGrab.grab()
    # 查找要点击的位置信息
    center = recog_img(screen_shot,os.path.join(PIC_DIR,'test1.png'))

    # 操作
    pyautogui.click(center)
    pyautogui.press('enter')
    pyautogui.press('enter')
    text = 'Auto INPUT time:' + NOW + 'Position:' + str(center)
    pyautogui.typewrite(text,interval=0.05)
    print(f'Total time consumed(总耗时): {time.perf_counter() - timer_start:.8f}s')
