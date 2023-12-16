import json
import os
import random
import sys
import time
import requests
import tkinter as tk
from tkinter import messagebox


class PickName:
    def __init__(self, root):
        # 版本信息
        version = 'v1.3.1'
        version_time = '2023.12.16'
        self.config_version = '1.1.0'

        # 初始名单
        self.names = [
            "陈佳绮", "邓佳丽", "邓欣悦", "邓颖欣", "段苏琴", "樊志杰", "龚雨轩", "胡思威", "胡雪颖",
            "黄煜鑫", "姜文涛", "李芳仪", "李佳亮", "李钦", "刘晨", "刘恩泉", "刘圣洋", "罗星", "马可欣",
            "浦睿", "孙健豪", "陶宸皓", "涂淑淇", "万宸希", "万晨欣", "万心悦", "万梓鑫", "王浩然", "王艺佳",
            "吴雨馨", "徐嘉铭", "徐楠", "徐腾宇", "徐媛轩", "许隆劲", "杨可心", "余思妍", "余欣萌", "袁子扬",
            "张睿", "张燕", "张濯铮", "章怡宸", "章轶琛", "赵梓霖", "周翔", "朱思静", "朱田茜", "祝馨怡"
        ]
        # self.names = ['a', 'b', 'c', 'd']

        # 初始化已抽取的名字列表
        self.can_pick_names = self.names.copy()

        # 初始化变量
        self.pick_again = False
        self.animation = True
        self.recite = False
        self.animation_time = 1.0
        self.picked_count = 0
        self.wait_recite_time = 5

        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.root = root
        self.selected_name = ''

        # 检查更新
        try:
            response = requests.get("https://api.github.com/repos/Chengzi600/GetBilibiliSpaceInfo/releases/latest")
            latest_version = response.json()['tag_name']
            latest_version_info = response.json()['body']
        except requests.exceptions:
            latest_version = '99.99.99'
            latest_version_info = '99.99.99'

        # 窗口初始化
        if latest_version != version:
            if latest_version == '99.99.99':
                self.root.title("【检查更新失败】点名程序(81专用) - 版本:{} - 编译日期:{}".format(version, version_time))
            else:
                self.root.title(
                    "【发现新版本-{}-{}】点名程序(81专用) - 版本:{} - 编译日期:{}".format(latest_version, latest_version_info,
                                                                                          version, version_time))
                self.root.geometry("1000x490")
        else:
            self.root.title("【已是最新版本】点名程序(81专用) - 版本:{} - 编译日期:{}".format(version, version_time))
            self.root.geometry("700x490")

        self.root.resizable(False, False)

        # 姓名显示区域
        self.name_label = tk.Label(self.root, text="请抽取", font=("宋体", 85))
        self.name_label.pack(pady=30)

        # 计时器显示区域
        self.timer_label = tk.Label(self.root, text="0.0s", font=('宋体', 40))

        # 抽取名字按钮
        self.pick_name_button = tk.Button(self.root, text="抽取名字", command=self.pick_name, font=("黑体", 25),
                                          bg='yellow')
        self.pick_name_button.pack()

        # 重置按钮
        self.reset_button = tk.Button(self.root, text="重置已抽取名单", command=self.reset, font=("黑体", 20), fg='red')
        self.reset_button.pack()

        # 复选框，是否背书模式
        self.recite_var = tk.BooleanVar()
        self.repeat_checkbox = tk.Checkbutton(self.root, text="背书模式(测试版)", command=self.set_recite,
                                              font=("宋体", 15), variable=self.recite_var)
        self.repeat_checkbox.pack()

        # 复选框，是否重复抽取
        self.pick_again_var = tk.BooleanVar()
        self.repeat_checkbox = tk.Checkbutton(self.root, text="允许重复抽取", command=self.set_pick_again,
                                              font=("宋体", 15), variable=self.pick_again_var)
        self.repeat_checkbox.pack()

        # 复选框，是否显示动画
        self.pick_animation_var = tk.BooleanVar()
        self.repeat_checkbox = tk.Checkbutton(self.root, text="开启动画", command=self.set_animation,
                                              font=("宋体", 15), variable=self.pick_animation_var)
        self.repeat_checkbox.pack()

        # 统计标签
        self.stats_label = tk.Label(self.root, text="统计信息获取中...", font=("宋体", 15))
        self.stats_label.pack(side='bottom')

        # 初始化
        self.read_config()
        self.update_stats()

    # 配置文件读取
    def read_config(self):
        try:
            os.makedirs('./dianming/', exist_ok=True)
            file_dir = r'./dianming/config.json'
            config_v = {
                'pick_again': self.pick_again,
                'animation': self.animation,
                'animation_time': self.animation_time,
                'can_pick_names': self.names,
                'picked_count': self.picked_count,
                'config_version': self.config_version
            }
            try:
                with open(file_dir) as config_file:
                    config = json.load(config_file)
                    if not config['config_version'] == self.config_version:
                        messagebox.showwarning('警告',
                                               '配置文件过时! 该版本的配置文件格式与当前不符\n请删除本程序的配置文件夹，然后重启程序！')
                        sys.exit('CONFIG_OUT_OF_DATE')

                    self.pick_again = config['pick_again']
                    self.animation = config['animation']
                    self.animation_time = config['animation_time']
                    self.can_pick_names = config['can_pick_names']
                    self.picked_count = config['picked_count']
                    self.pick_again_var.set(self.pick_again)
                    self.pick_animation_var.set(self.animation)

            except FileNotFoundError as e:
                with open(file_dir, 'w+') as config_file:
                    json.dump(config_v, config_file)
                # with open(file_dir) as config_file_r:
                # config = json.load(config_file_r)
                # config_d = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))
                messagebox.showinfo('提示', '配置文件创建成功!\n请重启程序!')
                print(e)
                sys.exit('CREATED_CONFIG_SUCCESSFULLY')
        except Exception as e:
            messagebox.showerror('错误',
                                 '配置文件创建或读取错误!\n请检查程序是否有对当前文件夹的读写权限\n可能配置文件已经损坏，请删除配置文件夹')
            sys.exit('FAILED_TO_LOAD_CONFIG')

    # 配置文件写入
    def save_config(self):
        try:
            file_dir = r'./dianming/config.json'
            with open(file_dir, 'r') as config_file:
                config = json.load(config_file)
                config['pick_again'] = self.pick_again
                config['animation'] = self.animation
                config['can_pick_names'] = self.can_pick_names
                config['picked_count'] = self.picked_count
            with open(file_dir, 'w') as config_file:
                json.dump(config, config_file)
        except Exception as e:
            messagebox.showerror('错误', '配置文件写入错误！')
            print(e)

    def set_pick_again(self):
        if not self.pick_again:
            self.pick_again = True
            tk.messagebox.showwarning('提示', '如切换至可重复模式，请点击重置，否则可能导致部分名字无法抽到!')
        elif self.pick_again:
            self.pick_again = False
        self.update_stats()

    def set_animation(self):
        if not self.animation:
            self.animation = True
        elif self.animation:
            self.animation = False

    def set_recite(self):
        if not self.recite:
            self.recite = True
            self.timer_label.pack(pady=5)

        elif self.recite:
            self.recite = False
            self.is_running = False
            self.timer_label.forget()

    def pick_name(self):

        self.is_running = False

        self.pick_name_button.config(state='disabled')
        self.reset_button.config(state='disabled')

        if not self.can_pick_names:
            messagebox.showinfo("提示", "所有名字已抽取完毕，请重置名单")
            self.name_label.config(text="请重置", fg='red')
            self.reset_button.config(state='normal')
            return

        self.selected_name = random.choice(self.can_pick_names)

        if self.animation:
            self.start_time = time.time()
            self.pick_animation()
        else:
            self.name_label.config(text=self.selected_name)
            self.pick_name_button.config(state='normal')
            self.reset_button.config(state='normal')
            if self.recite:
                self.is_running = False
                self.perform_countdown(self.wait_recite_time)

        if not self.pick_again:
            self.can_pick_names.remove(self.selected_name)

        # 更新统计信息
        self.picked_count += 1
        self.update_stats()
        self.save_config()

    def perform_countdown(self, seconds):
        self.pick_name_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        self.timer_label.config(fg="red")
        self.timer_label.config(text=f"{seconds:.1f}s")
        if seconds > 0:
            self.root.after(100, lambda: self.perform_countdown(seconds - 0.1))
        else:
            self.pick_name_button.config(state='normal')
            self.reset_button.config(state='normal')
            self.timer_label.config(fg="black")
            self.is_running = True
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"{self.elapsed_time:.1f}s")
            self.root.after(100, self.update_timer)

    def reset(self):
        if messagebox.askyesno('提示', '你确定要重置已抽取名单吗?'):
            if self.is_running:
                self.is_running = False
            if self.recite:
                self.timer_label.config(text="0.0s")
            self.can_pick_names = self.names.copy()
            self.name_label.config(text="请抽取", fg='black')
            self.pick_name_button.config(state='normal')
            self.save_config()
            self.update_stats()
            messagebox.showinfo("提示", "已清空已抽取名单!")
        else:
            return

    def pick_animation(self):
        if len(self.can_pick_names) <= 2:
            self.name_label.config(text=self.selected_name)
            self.pick_name_button.config(state='normal')
            self.reset_button.config(state='normal')
            return

        rdm_name = random.choice(self.can_pick_names)
        self.name_label.config(text=rdm_name)
        if time.time() - self.start_time < self.animation_time:  # x秒内不断变化
            root.after(10, self.pick_animation)  # 约x秒后再次调用change_text
        else:
            self.name_label.config(text=self.selected_name)
            self.pick_name_button.config(state='normal')
            self.reset_button.config(state='normal')
            if self.recite:
                self.is_running = False
                self.perform_countdown(self.wait_recite_time)
            return

    def update_stats(self):
        if not self.pick_again:
            try:
                self.stats_label.config(
                    text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n未抽者被抽概率: {}%".format(
                        len(self.names) - len(self.can_pick_names),
                        len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2)))
            except ZeroDivisionError:
                self.stats_label.config(
                    text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n未抽者被抽概率: {}%".format(
                        len(self.names) - len(self.can_pick_names),
                        len(self.can_pick_names), self.picked_count, '0'))
        else:
            self.stats_label.config(text="总抽取次数: {}".format(self.picked_count))


if __name__ == "__main__":
    root = tk.Tk()
    app = PickName(root)

    root.mainloop()
