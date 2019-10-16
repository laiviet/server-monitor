from tkinter import *
from util import *
import time


class PerformanceFrame():
    def __init__(self, master, col, controller):
        super(PerformanceFrame, self).__init__()
        self.controller = controller
        w1 = Frame(master)
        w1.grid(row=0, column=col)
        self.hostname_box = Text(w1, height=1, width=80)
        frame_title = controller.name + '-' + controller.hostname
        self.hostname_box.insert(END, frame_title, 'center')
        self.hostname_box.tag_add("center", "1.0", "end")
        self.cpu = Text(w1, height=21, width=80, bg='black', fg='yellow')
        self.gpu = Text(w1, height=35, width=80, bg='black', fg='yellow')
        self.hostname_box.pack()
        self.cpu.pack()
        self.gpu.pack()
        self.sleep = 1000

        self.cpu_ready = False
        self.gpu_ready = False

        self.update_cpu()
        self.update_gpu()

    def update_cpu(self):
        if self.cpu_ready:
            self.cpu.delete(1.0, END)
            self.cpu.insert(END, self.controller.cpu_usage)
            self.cpu.after(self.sleep, self.update_cpu)
        else:
            self.cpu.insert(END, self.controller.hostname)
            self.cpu_ready = True
            self.cpu.after(self.sleep, self.update_cpu)

    def update_gpu(self):
        if self.gpu_ready:
            self.gpu.delete(1.0, END)
            self.gpu.insert(END, self.controller.gpu_usage)
            self.gpu.after(self.sleep, self.update_gpu)
        else:
            self.gpu.insert(END, self.controller.hostname)
            self.gpu_ready = True
            self.gpu.after(self.sleep, self.update_gpu)


def quit():
    global root, controllers
    root.destroy()
    for i in range(len(controllers)):
        controllers[i].stop = True


root = Tk()
root.protocol("WM_DELETE_WINDOW", quit)
root.title('Server performance')

config = load_config()
controllers = [Controller(x) for x in config['server']]
for c in controllers:
    c.start()

frames = [PerformanceFrame(root, i, x) for i, x in enumerate(controllers)]

mainloop()
