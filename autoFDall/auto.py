import pyautogui
from time import sleep
import numpy as np
import cv2
from time import time

DEBUG = False
info = 'init'
mark = '+'
resRate = 1
opTime = time()


def switchMark():
    global mark
    mark = '-' if mark == '+' else '+'


def log(buf):
    global info
    global mark
    global opTime
    if time() - opTime > 120:
        pyautogui.press('1')
        opTime = time()
    if buf != info:
        opTime = time()
        info = buf
        print(f'\n  {info}', end='')
    else:
        print(f'\r{mark}', end='')
        switchMark()


def match(template_name, ac=0.85):
    img = pyautogui.screenshot()
    open_cv_image = np.array(img)
    img_gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(f'./{template_name}.png', 0)
    if template is None:
        print(f"Error: Template {template_name}.png not found!")
        return []
    x, y = template.shape[0:2]
    template = cv2.resize(template, (int(y * resRate), int(x * resRate)))
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= ac)
    locations = list(zip(*loc[::-1]))
    if DEBUG:
        print(locations)
    return locations






def start():
    pos_list = match('start')
    if pos_list:
        pos = pos_list[0]  # 获取第一个位置
        pyautogui.moveTo(pos[0] + 20, pos[1] + 20)  # 左上角向右下角偏移20像素
        pyautogui.leftClick()
        wait(0.1)
        pyautogui.leftClick()

def wait(sec):
    sleep(sec / 2)


def ready_to_cum():
    cum1_positions = match('cum1')
    cum2_positions = match('cum2')
    cum3_positions = match('cum3')
    return cum1_positions + cum2_positions + cum3_positions



def ready_to_start():
    return match('start')


def ready_to_finish():
    return match('finish')


def cum():
    pos_list = ready_to_cum()
    while not pos_list:  # Retry until positions are found
        log('未能cum')
        wait(0.2)
        pos_list = ready_to_cum()

    if pos_list:  # 检查列表是否为空
        pos = pos_list[0]  # 获取第一个位置
        pyautogui.moveTo(pos[0] + 20, pos[1] + 20)  # 左上角向右下角偏移20像素
        pyautogui.leftClick()
        wait(0.1)
        pyautogui.leftClick()


def finish():
    pos_list = match('finish')  # 这里使用 match 函数来查找 'finish' 图片的位置
    while not pos_list:  # 重试直到找到位置
        log('等待结束')
        wait(0.2)
        pos_list = match('finish')

    if pos_list:
        pos = pos_list[0]  # 获取第一个位置
        pyautogui.moveTo(pos[0] + 20, pos[1] + 20)  # 左上角向右下角偏移20像素
        pyautogui.leftClick()
        wait(0.1)
        pyautogui.leftClick()




def give():
    win = pyautogui.getWindowsWithTitle('FallenDoll')[0]
    x, y = win.left, win.top
    pyautogui.moveTo(x + 270 * resRate, y + 268 * resRate)
    pyautogui.leftClick()
    wait(0.1)
    pyautogui.moveTo(x + 125 * resRate, y + 330 * resRate)
    wait(0.1)
    pyautogui.leftClick()
    wait(0.1)
    pyautogui.leftClick()
    wait(0.1)
    pyautogui.moveTo(x + 270 * resRate, y + 378 * resRate)
    pyautogui.leftClick()
    wait(0.1)
    pyautogui.moveTo(x + 125 * resRate, y + 400 * resRate)
    wait(0.1)
    pyautogui.leftClick()
    wait(0.1)
    pyautogui.leftClick()
    wait(0.1)

loop_count = 0  # 放在函数定义之外的全局作用域

def loop():
    global loop_count
    loop_count += 1  # 每次进入 loop 函数时增加计数器

    while not ready_to_start():
        log('未找到开始')
        wait(0.2)
    while ready_to_start():
        start()
        pyautogui.moveRel(50 * resRate, 50 * resRate)
        log('点击开始')
        wait(0.2)

    while not ready_to_cum():
        log('未能cum')
        wait(0.2)
    while ready_to_cum():
        cum()
        pyautogui.moveRel(50 * resRate, 50 * resRate)
        log('cum')
        wait(0.2)

    while not ready_to_finish():
        log('等待结束')
        wait(0.2)
    while ready_to_finish():
        finish()
        pyautogui.moveRel(50 * resRate, 50 * resRate)
        log('结束')
        wait(0.2)
    if loop_count == 3:  # 当 loop 循环执行了三次时执行 give 命令
        give()
        loop_count = 0  # 重置 loop 计数器为零


if __name__ == '__main__':
    while True:
        loop()