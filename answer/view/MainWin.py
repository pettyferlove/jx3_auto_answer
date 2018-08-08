import tkinter
from PIL import ImageGrab
import win32api

def hello_call_back():
    print("Hello Python", "Hello Runoob")


def init_view():
    window = tkinter.Tk()
    window.title("剑网三自动答题器")
    window.geometry("700x400")
    btn_one = tkinter.Button(text="sss", command=hello_call_back)
    btn_print_screen = tkinter.Button(text="截取屏幕", command=print_screen)
    btn_one.pack()
    btn_print_screen.pack()
    window.mainloop()


def print_screen():
    ImageGrab.grab((300, 100, 1400, 600)).show()
