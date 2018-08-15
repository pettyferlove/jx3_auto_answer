import threading
from PIL import ImageGrab
from win32api import GetSystemMetrics
from answer.api.OcrApi import query_api
from io import BytesIO
import win32con
import tkinter
import sys
import ctypes
import ctypes.wintypes

lab_message = None
user32 = ctypes.windll.user32
id1 = 105
id2 = 106

posx1 = int(GetSystemMetrics(0) * 0.040625)
posy1 = int(GetSystemMetrics(1) * 0.25)
posx2 = int(GetSystemMetrics(0) * 0.410625)
posy2 = int(GetSystemMetrics(1) * 0.32)
showx = int(GetSystemMetrics(0) * 0.05625)
showy = int(GetSystemMetrics(1) * 0.5)


def print_screen():
    img = ImageGrab.grab((posx1, posy1, posx2, posy2))
    byte_data = BytesIO()
    img.save(byte_data, format="JPEG")
    byte_data = byte_data.getvalue()
    text = query_api(byte_data)
    register_lab(lab_message)
    BindKey().start()
    print(text)


def register_lab(lab):
    global lab_message
    lab_message = lab


class BindKey(threading.Thread):

    def run(self):
        window = tkinter.Tk()
        user32.UnregisterHotKey(None, id1)
        user32.UnregisterHotKey(None, id2)
        if not user32.RegisterHotKey(None, id1, 0, win32con.VK_F9):  # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。
            window.destroy()
            sys.exit()
        if not user32.RegisterHotKey(None, id2, 0, win32con.VK_F10):  # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。
            window.destroy()
            sys.exit()

        try:
            msg = ctypes.wintypes.MSG()

            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == id1:
                            lab_message['text'] = '开始监听'
                            print_screen()
                            print('开始')
                        elif msg.wParam == id2:
                            print('关闭')

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            user32.UnregisterHotKey(None, id1)
            user32.UnregisterHotKey(None, id2)
