import tkinter
from answer.common.Data import qst
from answer.common.BindKey import BindKey, register_lab

lab_message = None


def init_view():
    global lab_message
    print(qst[0])
    window = tkinter.Tk()
    window.title("剑网三自动答题器")
    window.geometry("400x200")
    lab_message = tkinter.Label(window, text='\n\n欢迎使用剑网三智能答题器')
    btn_print_screen = tkinter.Button(window, text="截取屏幕", command=print_screen, width=20, height=2)
    lab_message.pack()
    btn_print_screen.pack()
    window.mainloop()


def print_screen():
    register_lab(lab_message)
    BindKey().start()
