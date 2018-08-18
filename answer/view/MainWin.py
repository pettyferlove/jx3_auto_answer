import threading
from PIL import ImageGrab
from win32api import GetSystemMetrics
from answer.api.OcrApi import query_api
from answer.api.AnswerApi import answer_query
from io import BytesIO
import win32con
import tkinter
import sys
import ctypes
import ctypes.wintypes

lab_message = None
IS_BIND = False
user32 = ctypes.windll.user32
id1 = 105
id2 = 106

posx1 = int(GetSystemMetrics(0) * 0.040625)
posy1 = int(GetSystemMetrics(1) * 0.25)
posx2 = int(GetSystemMetrics(0) * 0.410625)
posy2 = int(GetSystemMetrics(1) * 0.568)
showx = int(GetSystemMetrics(0) * 0.05625)
showy = int(GetSystemMetrics(1) * 0.5)


def init_view():
    global lab_message
    window = tkinter.Tk()
    window.title("剑网三自动答题器")
    window.geometry("400x200")
    lab_title = tkinter.Label(window, text='\n\n欢迎使用剑网三智能答题器\n')
    lab_message = tkinter.Label(window, text='\n未开启按键监听')
    lab_title.pack()
    lab_message.pack()
    t = BindKey()
    t.setDaemon(True)
    t.start()
    window.mainloop()


def start_screen():
    img = ImageGrab.grab((posx1, posy1, posx2, posy2))
    byte_data = BytesIO()
    img.save(byte_data, format="JPEG")
    byte_data = byte_data.getvalue()
    result = query_api(byte_data)
    img_point = answer_query(result)
    print(img_point['answer'])
    print(img_point['btn'])
    img.show()


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
                            lab_message['text'] = '\n开始自动答题'
                            start_screen()
                        elif msg.wParam == id2:
                            lab_message['text'] = '\n关闭自动答题'

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            lab_message['text'] = '\n按键监听失败，请检查热键热键是否被占用'
            user32.UnregisterHotKey(None, id1)
            user32.UnregisterHotKey(None, id2)
