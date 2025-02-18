import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from input_simulator import InputSimulator
import time
import threading
import keyboard
import json
import os

class HotkeyDialog(tk.Toplevel):
    def __init__(self, parent, title, current_hotkey):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        
        self.result = None
        self.current_hotkey = current_hotkey
        
        self.setup_ui()
        
        # 对话框位置
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                 parent.winfo_rooty() + 50))
        
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind('<Key>', self.on_key)
        
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="请按下新的快捷键组合:").pack(pady=5)
        
        self.hotkey_var = tk.StringVar(value=self.current_hotkey)
        self.hotkey_entry = ttk.Entry(main_frame, textvariable=self.hotkey_var, 
                                    state='readonly', width=20)
        self.hotkey_entry.pack(pady=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="确定", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
    def on_key(self, event):
        if event.keysym in ('Escape', 'Return', 'space'):
            return
            
        mods = []
        if event.state & 0x4:
            mods.append('ctrl')
        if event.state & 0x8:
            mods.append('alt')
        if event.state & 0x1:
            mods.append('shift')
            
        key = event.keysym.lower()
        if key not in mods:
            mods.append(key)
            
        if mods:
            self.hotkey_var.set('+'.join(mods))
            
    def ok(self):
        self.result = self.hotkey_var.get()
        self.destroy()
        
    def cancel(self):
        self.destroy()

class InputSimulatorGUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("输入模拟器")
        self.root.geometry("800x600")
        
        self.simulator = InputSimulator()
        self.is_running = False
        
        # 加载配置
        self.config_file = "config.json"
        self.load_config()
        
        # 注册全局快捷键
        self.register_hotkeys()
        
        self.setup_ui()
        
    def load_config(self):
        default_config = {
            "start_hotkey": "ctrl+alt+s",
            "stop_hotkey": "ctrl+alt+x"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            
        self.start_hotkey = self.config.get("start_hotkey", "ctrl+alt+s")
        self.stop_hotkey = self.config.get("stop_hotkey", "ctrl+alt+x")
        
    def save_config(self):
        self.config["start_hotkey"] = self.start_hotkey
        self.config["stop_hotkey"] = self.stop_hotkey
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showwarning("警告", f"保存配置失败: {str(e)}")
            
    def register_hotkeys(self):
        try:
            keyboard.unhook_all()  # 清除所有快捷键
            keyboard.add_hotkey(self.start_hotkey, self.toggle_input)
            keyboard.add_hotkey(self.stop_hotkey, self.stop_input)
        except Exception as e:
            messagebox.showwarning("警告", f"注册快捷键失败: {str(e)}")
    
    def setup_ui(self):
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 左侧面板
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 右侧面板
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 文本输入区域
        input_frame = ttk.LabelFrame(self.left_panel, text="文本输入设置", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.text_input = tk.Text(input_frame, width=40, height=15)
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.text_input.bind('<KeyRelease>', self.on_text_change)
        
        # 选项区域
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # 输入模式选择
        mode_frame = ttk.LabelFrame(options_frame, text="输入模式", padding="5")
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 快速模式选项
        self.fast_mode_var = tk.BooleanVar(value=True)
        self.fast_mode_check = ttk.Radiobutton(
            mode_frame,
            text="快速模式",
            variable=self.fast_mode_var,
            value=True,
            command=self.on_input_mode_changed
        )
        self.fast_mode_check.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # 普通模式选项
        self.normal_mode_check = ttk.Radiobutton(
            mode_frame,
            text="普通模式",
            variable=self.fast_mode_var,
            value=False,
            command=self.on_input_mode_changed
        )
        self.normal_mode_check.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 输入法选项（仅在普通模式下可用）
        self.use_ime_var = tk.BooleanVar(value=False)
        self.use_ime_check = ttk.Checkbutton(
            mode_frame,
            text="使用系统输入法",
            variable=self.use_ime_var,
            state=tk.DISABLED
        )
        self.use_ime_check.grid(row=0, column=2, sticky=tk.W, padx=20)
        
        # 格式选项
        self.keep_format_var = tk.BooleanVar(value=True)
        self.keep_format_check = ttk.Checkbutton(
            options_frame, 
            text="保持原文格式",
            variable=self.keep_format_var
        )
        self.keep_format_check.grid(row=1, column=0, sticky=tk.W)
        
        # 循环选项
        self.loop_var = tk.BooleanVar(value=False)
        self.loop_check = ttk.Checkbutton(
            options_frame,
            text="循环输入",
            variable=self.loop_var
        )
        self.loop_check.grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
        
        # 编码选择
        encoding_frame = ttk.Frame(options_frame)
        encoding_frame.grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Label(encoding_frame, text="编码:").grid(row=0, column=0)
        self.encoding_var = tk.StringVar(value="utf-8")
        self.encoding_combo = ttk.Combobox(
            encoding_frame,
            textvariable=self.encoding_var,
            values=["utf-8", "gbk", "gb2312", "ascii"],
            state="readonly",
            width=8
        )
        self.encoding_combo.grid(row=0, column=1, padx=5)

        # 间隔设置区域
        interval_frame = ttk.LabelFrame(options_frame, text="输入间隔", padding="5")
        interval_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(interval_frame, text="输入模式:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="固定间隔")
        mode_combo = ttk.Combobox(interval_frame, textvariable=self.mode_var, 
                                 values=["固定间隔", "随机间隔"], state="readonly", width=10)
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_changed)
        
        # 间隔设置
        self.interval_frame = ttk.Frame(interval_frame)
        self.interval_frame.grid(row=0, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(self.interval_frame, text="间隔(秒):").grid(row=0, column=0)
        self.interval_var = tk.DoubleVar(value=0.1)
        self.interval_spin = ttk.Spinbox(self.interval_frame, from_=0.01, to=10.0, 
                                       increment=0.1, width=5, textvariable=self.interval_var)
        self.interval_spin.grid(row=0, column=1, padx=5)
        
        # 随机间隔设置
        self.random_frame = ttk.Frame(interval_frame)
        self.random_frame.grid(row=0, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(self.random_frame, text="最小间隔:").grid(row=0, column=0)
        self.min_interval_var = tk.DoubleVar(value=0.1)
        self.min_interval_spin = ttk.Spinbox(self.random_frame, from_=0.01, to=10.0,
                                           increment=0.1, width=5, textvariable=self.min_interval_var)
        self.min_interval_spin.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.random_frame, text="最大间隔:").grid(row=0, column=2)
        self.max_interval_var = tk.DoubleVar(value=0.3)
        self.max_interval_spin = ttk.Spinbox(self.random_frame, from_=0.01, to=10.0,
                                           increment=0.1, width=5, textvariable=self.max_interval_var)
        self.max_interval_spin.grid(row=0, column=3, padx=5)

        # 统计信息区域
        self.stats_frame = ttk.LabelFrame(self.right_panel, text="文本统计", padding="5")
        self.stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.stats_labels = {}
        stats_items = [
            ('total_chars', '总字数：'),
            ('chars_no_spaces', '不含空格字数：'),
            ('chinese_chars', '中文字数：'),
            ('english_words', '英文单词数：'),
            ('punctuation', '标点符号数：'),
            ('spaces', '空格数：'),
            ('lines', '行数：')
        ]
        
        for i, (key, text) in enumerate(stats_items):
            label = ttk.Label(self.stats_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.W)
            value_label = ttk.Label(self.stats_frame, text="0")
            value_label.grid(row=i, column=1, sticky=tk.W)
            self.stats_labels[key] = value_label
        
        # 问题列表区域
        self.issues_frame = ttk.LabelFrame(self.right_panel, text="潜在问题", padding="5")
        self.issues_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.issues_text = tk.Text(self.issues_frame, width=30, height=10, wrap=tk.WORD)
        self.issues_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        self.issues_scrollbar = ttk.Scrollbar(self.issues_frame, orient=tk.VERTICAL, command=self.issues_text.yview)
        self.issues_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.issues_text.configure(yscrollcommand=self.issues_scrollbar.set)
        
        # 快捷键设置区域
        hotkey_frame = ttk.LabelFrame(self.left_panel, text="快捷键设置", padding="5")
        hotkey_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        start_hotkey_frame = ttk.Frame(hotkey_frame)
        start_hotkey_frame.grid(row=0, column=0, padx=5)
        ttk.Label(start_hotkey_frame, text="开始/暂停:").grid(row=0, column=0, sticky=tk.W)
        self.start_hotkey_label = ttk.Label(start_hotkey_frame, text=self.start_hotkey)
        self.start_hotkey_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(start_hotkey_frame, text="修改", 
                  command=lambda: self.change_hotkey("开始/暂停快捷键", "start_hotkey")
                  ).grid(row=0, column=2, sticky=tk.E, padx=5)
        
        stop_hotkey_frame = ttk.Frame(hotkey_frame)
        stop_hotkey_frame.grid(row=1, column=0, padx=5)
        ttk.Label(stop_hotkey_frame, text="停止:").grid(row=1, column=0, sticky=tk.W)
        self.stop_hotkey_label = ttk.Label(stop_hotkey_frame, text=self.stop_hotkey)
        self.stop_hotkey_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(stop_hotkey_frame, text="修改",
                  command=lambda: self.change_hotkey("停止快捷键", "stop_hotkey")
                  ).grid(row=1, column=2, sticky=tk.E, padx=5)
        
        # 控制按钮区域
        control_frame = ttk.Frame(self.left_panel)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.start_btn = ttk.Button(control_frame, text="开始输入", command=self.toggle_input)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="停止", command=self.stop_input, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(self.left_panel, textvariable=self.status_var)
        status_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.on_mode_changed(None)
        
    def change_hotkey(self, title, hotkey_type):
        current_hotkey = getattr(self, hotkey_type)
        dialog = HotkeyDialog(self.root, title, current_hotkey)
        self.root.wait_window(dialog)
        
        if dialog.result:
            setattr(self, hotkey_type, dialog.result)
            if hotkey_type == "start_hotkey":
                self.start_hotkey_label.config(text=dialog.result)
            else:
                self.stop_hotkey_label.config(text=dialog.result)
                
            self.save_config()
            self.register_hotkeys()
        
    def toggle_input(self):
        if not self.is_running:
            self.start_input()
        else:
            self.stop_input()
            
    def on_mode_changed(self, event):
        """处理输入模式改变事件"""
        if self.mode_var.get() == "固定间隔":
            self.interval_frame.grid(row=0, column=2, sticky=tk.W, padx=5)
            self.random_frame.grid_remove()
        else:
            self.interval_frame.grid_remove()
            self.random_frame.grid(row=0, column=2, sticky=tk.W, padx=5)
            
    def start_input(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入要模拟的文本！")
            return
            
        self.start_btn.config(text="暂停")
        self.text_input.config(state=tk.DISABLED)
        self.loop_check.config(state=tk.DISABLED)
        self.status_var.set("3秒后开始输入...")
        
        def countdown():
            time.sleep(3)
            self.perform_input(text)
            
        threading.Thread(target=countdown, daemon=True).start()
        
    def perform_input(self, text):
        self.is_running = True
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("正在输入...")
        
        def input_thread():
            try:
                # 处理文本格式
                if not self.keep_format_var.get():
                    # 不保持格式时，将多个空格和换行转换为单个空格
                    text_to_input = ' '.join(text.split())
                else:
                    text_to_input = text
                
                encoding = self.encoding_var.get()
                use_ime = self.use_ime_var.get()
                fast_mode = self.fast_mode_var.get()
                
                if self.mode_var.get() == "固定间隔":
                    interval = self.interval_var.get()
                    self.simulator.start_continuous_input(text_to_input, interval, 
                                                       self.loop_var.get(), encoding, 
                                                       use_ime, fast_mode)
                else:
                    min_interval = self.min_interval_var.get()
                    max_interval = self.max_interval_var.get()
                    self.simulator.start_continuous_input(text_to_input, 
                                                       (min_interval, max_interval),
                                                       self.loop_var.get(), encoding, 
                                                       use_ime, fast_mode)
                
                # 如果不是循环模式，输入完成后自动停止
                if not self.loop_var.get():
                    self.root.after(0, self.stop_input)
                    self.root.after(0, lambda: self.status_var.set("输入完成"))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"输入过程出错: {str(e)}"))
                self.root.after(0, self.stop_input)
                
        threading.Thread(target=input_thread, daemon=True).start()
        
    def stop_input(self):
        self.simulator.stop()
        self.is_running = False
        self.start_btn.config(text="开始输入", state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.text_input.config(state=tk.NORMAL)
        self.loop_check.config(state=tk.NORMAL)
        if self.status_var.get() != "输入完成":
            self.status_var.set("已停止")
        
    def on_text_change(self, event=None):
        """当文本内容改变时更新统计信息"""
        text = self.text_input.get("1.0", tk.END)
        analysis = self.simulator.analyze_text(text)
        
        # 更新统计信息
        for key, value in analysis['stats'].items():
            if key in self.stats_labels:
                self.stats_labels[key].configure(text=str(value))
        
        # 更新问题列表
        self.issues_text.delete("1.0", tk.END)
        if analysis['issues']:
            for issue in analysis['issues']:
                issue_text = f"• {issue['type']} (位置 {issue['position']})\n"
                issue_text += f"  {issue['description']}\n"
                issue_text += f"  内容: {issue['content']}\n\n"
                self.issues_text.insert(tk.END, issue_text)
        else:
            self.issues_text.insert(tk.END, "未发现问题")
        
    def on_input_mode_changed(self):
        """处理输入模式改变事件"""
        if self.fast_mode_var.get():
            self.use_ime_check.config(state=tk.DISABLED)
            self.use_ime_var.set(False)
        else:
            self.use_ime_check.config(state=tk.NORMAL)
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        if self.is_running:
            self.stop_input()
        # 清理快捷键
        keyboard.unhook_all()
        self.root.destroy()

if __name__ == "__main__":
    app = InputSimulatorGUI()
    app.run() 