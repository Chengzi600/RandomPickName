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
        self.version = 'v1.3.5'
        self.version_time = '2024.6.10'
        self.version_info = '81专用'
        self.config_version = '1.1.3'

        # 初始名单
        self.names = [
            "邓颖欣", "姜文涛", "樊志杰", "马可欣", "陈佳绮", "黄朝伟", "余欣萌", "孙健豪", "刘晨", "黄煜鑫",
            "龚雨轩", "袁子扬", "徐媛轩", "胡雪颖", "李钦", "浦睿", "许隆劲", "刘圣洋", "刘恩泉", "邓欣悦",
            "徐楠", "涂淑淇", "余思妍", "万心悦", "魏博", "李佳亮", "徐腾宇", "周翔", "万晨欣", "张睿",
            "胡思威", "朱思静", "章轶琛", "朱田茜", "李芳仪", "张濯铮", "段苏琴", "陶宸皓", "郭光星", "祝馨怡",
            "刘思洁", "王佳鹏", "章怡宸", "徐嘉铭", "罗星", "张燕", "王浩然", "赵梓霖", "杨可心"
        ]
        self.g_names = [
            "陈佳绮", "邓颖欣", "邓欣悦", "段苏琴", "龚雨轩",
            "胡雪颖", "李芳仪", "马可欣",
            "涂淑淇", "万晨欣", "万心悦",
            "徐楠", "徐媛轩", "杨可心", "余思妍", "余欣萌", "张燕",
            "张濯铮", "朱思静", "朱田茜", "祝馨怡", "章怡宸", "刘思洁"
        ]
        self.b_names = [
            '樊志杰', '胡思威', '黄煜鑫', '姜文涛', '刘恩泉', '刘圣洋', '罗星', '浦睿',
            '孙健豪', '陶宸皓', '徐嘉铭', '徐腾宇', '许隆劲', '袁子扬',
            '张睿', '章轶琛', '赵梓霖', '周翔', "李钦", "刘晨", "李佳亮", "王浩然", "魏博",
            "郭光星", "王佳鹏", "黄朝伟"

        ]
        # print(len(self.g_names)+len(self.b_names))
        # print(len(self.b_names))
        # print(len(self.b_names_bak))
        # print(len(self.names))
        # self.names = ['a', 'b', 'c', 'd']

        # 初始化已抽取的名字列表
        self.can_pick_names = self.names.copy()

        # 初始化变量
        self.pick_again = False
        self.animation = True
        self.recite = False
        self.is_save = False
        self.pick_only_g = False
        self.pick_only_b = False
        self.animation_time = 1.0
        self.picked_count = 0
        self.wait_recite_time = 3

        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.root = root
        self.selected_name = ''

        self.root.geometry("570x630")
        self.root.title(
            "点名程序({}) - 版本:{} - 编译日期:{}".format(self.version_info, self.version, self.version_time))
        self.root.resizable(False, False)

        # 姓名显示区域
        self.name_label = tk.Label(self.root, text="请抽取", font=("微软雅黑", 90))
        self.name_label.pack(pady=30)

        # 计时器显示区域
        self.timer_label = tk.Label(self.root, text="0.0s", font=('得意黑', 40))

        # 抽取名字按钮
        self.pick_name_button = tk.Button(self.root, text="   -->>抽取<<--   ", command=self.pick_name, font=("黑体", 30),
                                          bg='orange')
        self.pick_name_button.pack()

        # 创建空白区域
        self.blank_space1 = tk.Label(self.root, text="", font=("宋体", 2), fg='black')
        self.blank_space1.pack()

        # 重置按钮
        self.reset_button = tk.Button(self.root, text="    重置名单    ", command=self.reset, font=("黑体", 20), fg='red')
        self.reset_button.pack()

        # 创建空白区域
        self.blank_space2 = tk.Label(self.root, text="", font=("宋体", 15), fg='black')
        self.blank_space2.pack()
        self.blank_space3 = tk.Label(self.root, text="--配置区--", font=("得意黑", 15), fg='black')
        self.blank_space3.pack()

        # 创建一个复选框的框架容器 by GPT4o
        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack()

        # 创建复选框组 1 by GPT4o
        self.checkbox_group1 = tk.Frame(self.checkbox_frame)
        self.checkbox_group1.pack(anchor='center')

        # 创建复选框组 2 by GPT4o
        self.checkbox_group2 = tk.Frame(self.checkbox_frame)
        self.checkbox_group2.pack(anchor='center')

        # 创建复选框组 3 by GPT4o
        self.checkbox_group3 = tk.Frame(self.checkbox_frame)
        self.checkbox_group3.pack(anchor='center')

        # 复选框，是否保存
        self.is_save_var = tk.BooleanVar()
        self.is_save_var_checkbox = tk.Checkbutton(self.checkbox_group3, text="退出时保存", command=self.set_save,
                                                   font=("宋体", 15), variable=self.is_save_var, fg='purple')
        self.is_save_var_checkbox.pack(side='left')

        # 复选框，是否背书模式
        self.recite_var = tk.BooleanVar()
        self.recite_checkbox = tk.Checkbutton(self.checkbox_group1, text="计时器", command=self.set_recite,
                                              font=("宋体", 15), variable=self.recite_var, fg='brown')
        self.recite_checkbox.pack(side='left')

        # 复选框，是否只抽男/女
        self.g_names_pick_var = tk.BooleanVar()
        self.g_names_pick_checkbox = tk.Checkbutton(self.checkbox_group2, text="只抽女生",
                                                    command=self.set_pick_group_g,
                                                    font=("宋体", 15), variable=self.g_names_pick_var, fg='red')
        self.g_names_pick_checkbox.pack(side='left')

        self.b_names_pick_var = tk.BooleanVar()
        self.b_names_pick_checkbox = tk.Checkbutton(self.checkbox_group2, text="只抽男生",
                                                    command=self.set_pick_group_b,
                                                    font=("宋体", 15), variable=self.b_names_pick_var, fg='blue')
        self.b_names_pick_checkbox.pack(side='left')

        # 复选框，是否重复抽取
        self.pick_again_var = tk.BooleanVar()
        self.pick_again_checkbox = tk.Checkbutton(self.checkbox_group3, text="允许重复抽取",
                                                  command=self.set_pick_again,
                                                  font=("宋体", 15), variable=self.pick_again_var)
        self.pick_again_checkbox.pack(side='left')

        # 复选框，是否显示动画
        self.pick_animation_var = tk.BooleanVar()
        self.pick_animation_checkbox = tk.Checkbutton(self.checkbox_group3, text="开启动画", command=self.set_animation,
                                                      font=("宋体", 15), variable=self.pick_animation_var)
        self.pick_animation_checkbox.pack(side='left')

        # # 创建空白区域
        # self.blank_space4 = tk.Label(self.root, text="", font=("宋体", 15), fg='black')
        # self.blank_space4.pack()
        # self.blank_space5 = tk.Label(self.root, text="--统计信息--", font=("得意黑", 15), fg='black')
        # self.blank_space5.pack()

        # 统计标签
        self.stats_label = tk.Label(self.root, text="统计信息获取中...", font=("得意黑", 17), fg='green')
        self.stats_label.pack(side='bottom')

        # 初始化
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.read_config()
        self.update_stats()
        # self.check_update()

    # 配置文件读取
    def read_config(self):
        try:
            os.makedirs('./PickNameConfig/', exist_ok=True)
            file_dir = r'./PickNameConfig/config.json'
            config_v = {
                'pick_again': self.pick_again,
                'animation': self.animation,
                'animation_time': self.animation_time,
                'is_save': self.is_save,
                'picked_count': self.picked_count,
                'config_version': self.config_version,
                'can_pick_names': self.names,
            }
            try:
                with open(file_dir, encoding='utf-8') as config_file:
                    config = json.load(config_file)
                    if not config['config_version'] == self.config_version:
                        messagebox.showwarning('警告',
                                               '配置文件过时! 该版本的配置文件格式与当前不符\n请删除本程序的配置文件夹，然后重启程序！')
                        sys.exit('CONFIG_OUT_OF_DATE')

                    self.is_save = config['is_save']
                    self.is_save_var.set(self.is_save)
                    self.pick_again = config['pick_again']
                    self.animation = config['animation']
                    self.animation_time = config['animation_time']
                    self.can_pick_names = config['can_pick_names']
                    self.picked_count = config['picked_count']
                    self.pick_again_var.set(self.pick_again)
                    self.pick_animation_var.set(self.animation)

            except FileNotFoundError as e:
                with open(file_dir, 'w+', encoding='utf-8') as config_file:
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
            print("错误信息:", e)
            sys.exit('FAILED_TO_LOAD_CONFIG')

    # 配置文件写入
    def save_config(self):
        try:
            file_dir = r'./PickNameConfig/config.json'
            with open(file_dir, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                config['is_save'] = self.is_save
                config['pick_again'] = self.pick_again
                config['animation'] = self.animation
                if self.is_save:
                    config['can_pick_names'] = self.can_pick_names
                else:
                    config['can_pick_names'] = self.names
                config['picked_count'] = self.picked_count
            with open(file_dir, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror('错误', '配置文件写入错误！')
            print("配置文件写入错误:", e)

    def set_pick_again(self):
        if not self.pick_again:
            self.pick_again = True
            self.can_pick_names = self.names.copy()
            tk.messagebox.showinfo('提示', '切换成功,已清空已抽取名单')
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

    def set_save(self):
        if not self.is_save:
            self.is_save = True
        else:
            self.is_save = False

    def set_pick_group_g(self):
        if not self.pick_only_g:
            if messagebox.askyesno("继续吗",
                                   "该操作将清空已抽取的名字，继续吗？\n 这次将无法再使用重复抽取功能，如有需要请重启"):
                self.pick_again = False
                self.pick_again_var.set(False)
                self.pick_again_checkbox.config(state='disabled')
                self.pick_only_g = True
                self.set_pick_group('g')
                self.can_pick_names = self.g_names.copy()
                self.update_stats()
            else:
                self.g_names_pick_var.set(False)
        else:
            self.set_pick_group('clear')

    def set_pick_group_b(self):
        if not self.pick_only_b:
            if messagebox.askyesno("继续吗",
                                   "该操作将清空已抽取的名字，继续吗？\n 这次将无法再使用重复抽取功能，如有需要请重启"):
                self.pick_again = False
                self.pick_again_var.set(False)
                self.pick_again_checkbox.config(state='disabled')
                self.pick_only_b = True
                self.set_pick_group('b')
                self.can_pick_names = self.b_names.copy()
                self.update_stats()
            else:
                self.g_names_pick_var.set(False)
        else:
            self.set_pick_group('clear')

    def set_pick_group(self, ab):
        # 如果两个复选框都被选中，则取消另一个的选中状态
        if self.pick_only_b and self.pick_only_g:
            if ab == 'g':
                self.pick_only_b = False
                self.b_names_pick_var.set(False)
            elif ab == 'b':
                self.pick_only_g = False
                self.g_names_pick_var.set(False)
        elif ab == 'clear':
            self.pick_only_g = False
            self.g_names_pick_var.set(False)
            self.pick_only_b = False
            self.b_names_pick_var.set(False)
            self.can_pick_names = self.names.copy()
            self.update_stats()

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
        # self.save_config()

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

    def reset(self, no_tip=False):
        def perform_reset():
            if self.is_running:
                self.is_running = False
            if self.recite:
                self.timer_label.config(text="0.0s")
            self.set_pick_group('clear')
            self.can_pick_names = self.names.copy()
            self.name_label.config(text="请抽取", fg='black')
            self.pick_name_button.config(state='normal')
            self.save_config()
            self.update_stats()

        if no_tip:
            perform_reset()
        else:
            if messagebox.askyesno('提示', '你确定要重置已抽取名单吗?'):
                perform_reset()
                messagebox.showinfo("提示", "已清空已抽取名单!")

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
                if self.pick_only_g:
                    self.stats_label.config(
                        text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                            len(self.g_names) - len(self.can_pick_names),
                            len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2)))
                elif self.pick_only_b:
                    self.stats_label.config(
                        text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                            len(self.b_names) - len(self.can_pick_names),
                            len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2)))
                else:
                    self.stats_label.config(
                        text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                            len(self.names) - len(self.can_pick_names),
                            len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2)))

            except ZeroDivisionError:
                self.stats_label.config(
                    text="已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                        "抽完了",
                        len(self.can_pick_names), self.picked_count, '0'))
        else:
            self.stats_label.config(text="总抽取次数: {}".format(self.picked_count))

    def check_update(self):
        # 检查更新
        try:
            response = requests.get("https://api.github.com/repos/Chengzi600/RandomPickName/releases/latest")
            latest_version = response.json()['tag_name']
            latest_version_info = response.json()['body']
        except Exception as e:
            print('检查更新失败:', e)
            latest_version = '99.99.99'
            latest_version_info = '99.99.99'

        # 窗口操作
        if latest_version != self.version:
            if latest_version == '99.99.99':
                self.root.title(
                    "【检查更新失败】点名程序(81专用) - 版本:{} - 编译日期:{}".format(self.version, self.version_time))
            else:
                self.root.title(
                    "【发现新版本-{}-{}】点名程序(81专用) - 版本:{} - 编译日期:{}".format(
                        latest_version, latest_version_info, self.version, self.version_time))
                self.root.geometry("1000x490")
        else:
            self.root.title(
                "【已是最新版本】点名程序(81专用) - 版本:{} - 编译日期:{}".format(self.version, self.version_time))
            self.root.geometry("700x490")

    def on_closing(self):
        if self.pick_only_g or self.pick_only_b or self.pick_again:
            self.reset(no_tip=True)
            sys.exit()
        else:
            self.save_config()
            root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PickName(root)

    root.mainloop()
