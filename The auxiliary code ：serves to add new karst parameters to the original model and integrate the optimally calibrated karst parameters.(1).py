"""
Function

    Add new parameters to the  groundwater module file(.gw)


"""
import os
import win32api, win32con  # 用于弹出消息提示
import tkinter
from tkinter import *
import hashlib
import time


class SWAT_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name  # 主窗口初始化

    def set_init_window(self):
        self.init_window_name.title("SWAT岩溶改进辅助软件")  # 窗口名
        self.init_window_name.geometry('350x230+600+350')  # 550x1000为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_data_label = Label(self.init_window_name, text="输入数据区域")
        self.init_data_label.grid(row=0, column=1)
        self.init_belta_label = Label(self.init_window_name, text="       belta      ", bg="SlateGray")
        self.init_belta_label.grid(row=1, column=0)
        self.init_alpha1_label = Label(self.init_window_name, text=" alpha(matrix) ", bg="SlateGray")
        self.init_alpha1_label.grid(row=2, column=0)
        self.init_alpha2_label = Label(self.init_window_name, text="alpha(conduit)", bg="SlateGray")
        self.init_alpha2_label.grid(row=3, column=0)
        self.log_label = Label(self.init_window_name, text="执行提示窗口")
        self.log_label.grid(row=4, column=0)

        # 文本框
        self.init_belta_Text = Text(self.init_window_name, width=10, height=1)  # belta
        self.init_belta_Text.grid(row=1, column=1, rowspan=1, columnspan=1)
        self.init_alpha1_Text = Text(self.init_window_name, width=10, height=1)  # alpha1
        self.init_alpha1_Text.grid(row=2, column=1, columnspan=1)
        self.init_alpha2_Text = Text(self.init_window_name, width=10, height=1)  # alpha2
        self.init_alpha2_Text.grid(row=3, column=1, columnspan=1)
        self.log_log_Text = Text(self.init_window_name, width=30, height=5)  # 输出提示框
        self.log_log_Text.grid(row=5, column=1, columnspan=5)
        self.log_log_Text.insert(END, "保留四位小数\n"
                                      "① 程序并非通用程序。\n"
                                      "② belta、ALPHA_conduit、ALPHA_matrix 默认参数分别为0.7000、0.0500、0.0020", 'color')

        # 按钮
        self.add_karst_para_button = Button(self.init_window_name, text="添加岩溶参数", bg="lightblue", width=10,
                                              command=self.add_karst_para)  # 调用内部方法  加()为直接调用
        self.add_karst_para_button.grid(row=2, column=3)
        self.back_new_karst_para_button = Button(self.init_window_name, text="回代岩溶参数", bg="lightblue", width=10,
                                            command=self.back_new_para)  # 调用内部方法  加()为直接调用
        self.back_new_karst_para_button.grid(row=3, column=3)

    def add_karst_para(self):
        # --------实现参数添加部分代码------------------------
        file_path = os.getcwd()  # 获取当前文件位置
        print(file_path)
        name = os.listdir(file_path)  # 读取当前文件下所有文件
        add_1 = "          0.7000    | beta_n : the recharge separation factor,ranging from 0 to 1 [-]" + "\n"
        add_2 = "          0.0500    | ALPHA_conduit : the recession constant of the conduit storage reservoir[1/day]" + "\n"
        add_3 = "          0.0020    | ALPHA_matrix : the recession constant of the matrix storage reservoir [1/days]"
        # print(name)
        loop_status = 1
        for i in name:
            loop_status = 1
            if "gw" in i:  # 找到地下水模块的文件
                file_add_par = open(file_path + "\\" + i, "r", encoding="UTF-8")
                for line in file_add_par.readlines():
                    if "beta_n" in line:
                        # win32api.MessageBox(0, "The parameters were previously added successfully\n之前已经添加", "Message", win32con.MB_OK)
                        file_add_par.close()
                        loop_status = 0
                        continue
                file_add_par.close()  # 先将文件关闭
                if loop_status == 0:
                    continue
                file_add_par = open(file_path + "\\" + i, "a", encoding="UTF-8")  # "a" 代表追加内容,
                file_add_par.write(add_1 + add_2 + add_3)
                file_add_par.close()
            if loop_status == 0:
                break
        if loop_status == 1:
            win32api.MessageBox(0, "CBH  Parameters added successfully\n 岩溶改进参数添加成功", "Message", win32con.MB_OK)
        # --------实现参数添加部分代码------------------------

    def back_new_para(self):
        belta_new = self.init_belta_Text.get(1.0, END).strip().replace("\n", "")
        alpha_matrix = self.init_alpha1_Text.get(1.0, END).strip().replace("\n", "")
        alpha_conduit = self.init_alpha2_Text.get(1.0, END).strip().replace("\n", "")
        print(belta_new + belta_new, alpha_conduit, alpha_matrix)
        file_path = os.getcwd()

        with open(file_path + "\\" + "000010001.gw", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(file_path + "\\" + "000010001.gw", "w", encoding="utf-8") as f_w:
            for line in lines:
                if ("beta_n" in line) or ("ALPHA_conduit" in line) or ("ALPHA_matrix" in line):
                    continue
                f_w.write(line)
        f.close()
        add_1 = "          " + str(belta_new) + "    | beta_n : the recharge separation factor,ranging from 0 to 1 [-]" + "\n"
        add_2 = "          " + str(alpha_matrix) + "    | ALPHA_conduit : the recession constant of " \
                                              "the conduit storage reservoir[1/day]" + "\n"
        add_3 = "          " + str(alpha_conduit) + "    | ALPHA_matrix : the recession constant of the " \
                                               "matrix storage reservoir [1/days]"

        file_add_par = open(file_path + "\\" + "000010001.gw", "a", encoding="UTF-8")  # "a" 代表追加内容,
        file_add_par.write(add_1 + add_2 + add_3)
        file_add_par.close()
        win32api.MessageBox(0, "岩溶参数回代成功", "Message", win32con.MB_OK)


        # file_new_para = open(file_path + "\\" + "input_karst.txt", "w", encoding="UTF-8")
        # file_new_para.write(belta_new + "\n" + "0" + "\n" + alpha_matrix + " " + alpha_conduit)
        # file_new_para.close()


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = SWAT_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.resizable(False, False)
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()

# #  打包文件的指令为：pyinstaller -w -F add_parameters.py
