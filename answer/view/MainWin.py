import tkinter
from PIL import ImageGrab
from answer.common.data import qst
import win32api

def hello_call_back():
    print("Hello Python", "Hello Runoob")
from PIL import Image
from win32api import GetSystemMetrics
from answer.api.OcrApi import query_api
from io import BytesIO


def init_view():
    print(qst[0])
    window = tkinter.Tk()
    window.title("剑网三自动答题器")
    window.geometry("400x200")
    btn_print_screen = tkinter.Button(text="截取屏幕", command=print_screen)
    btn_print_screen.grid(row=4, column=2, columnspan=3)
    window.mainloop()


def print_screen():
    img = ImageGrab.grab((posx1, posy1, posx2, posy2))
    byte_data = BytesIO()
    img.save(byte_data, format="JPEG")
    byte_data = byte_data.getvalue()
    text = query_api(byte_data)
    print(text)


posx1 = int(GetSystemMetrics(0) * 0.040625)
posy1 = int(GetSystemMetrics(1) * 0.25)
posx2 = int(GetSystemMetrics(0) * 0.410625)
posy2 = int(GetSystemMetrics(1) * 0.32)
showx = int(GetSystemMetrics(0) * 0.05625)
showy = int(GetSystemMetrics(1) * 0.5)
