import os
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk, ImageFilter

class TaskEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("任务编辑器")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.LOG_FILE = "D:/getting/log.json"
        
        # 直接初始化主界面
        self.init_main_ui()
        
    def init_main_ui(self):
        """初始化主界面"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        
        # 加载已有任务
        self.tasks = self.load_tasks()
        
        # 创建UI
        self.create_widgets()
        
    def create_widgets(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#4a7abc", height=40)
        title_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(title_frame, text="开机任务编辑器", font=("微软雅黑", 16, "bold"), 
                fg="white", bg="#4a7abc").pack(pady=8)
        
        # 任务列表
        list_frame = tk.LabelFrame(self.root, text="任务列表 (支持拖放添加)", font=("微软雅黑", 10), 
                                 bg="#f0f0f0", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # 创建带滚动条的列表框
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.task_list = tk.Listbox(list_frame, width=80, height=12, font=("微软雅黑", 10),
                                  yscrollcommand=scrollbar.set, selectbackground="#a6d4ff")
        self.task_list.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.task_list.yview)
        
        # 添加拖放功能
        self.task_list.drop_target_register(DND_FILES)
        self.task_list.dnd_bind('<<Drop>>', self.drop)
        
        # 填充任务列表
        self.update_task_list()
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=15, pady=10)
        
        # 添加任务按钮
        add_btn = tk.Button(button_frame, text="添加任务", font=("微软雅黑", 10), 
                          bg="#4CAF50", fg="white", width=12, command=self.add_task)
        add_btn.pack(side="left", padx=10)
        
        # 删除任务按钮
        remove_btn = tk.Button(button_frame, text="删除任务", font=("微软雅黑", 10), 
                             bg="#f44336", fg="white", width=12, command=self.remove_task)
        remove_btn.pack(side="left", padx=10)
        
        # 底部信息
        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        info_text = "支持拖放添加任务: 将.py, .bat, .exe, .lnk文件拖放到任务列表中"
        tk.Label(info_frame, text=info_text, font=("微软雅黑", 9), fg="#666666", 
                bg="#f0f0f0").pack(side="left")
    
    def load_tasks(self):
        """从Base64编码的文件加载任务列表"""
        try:
            if os.path.exists(self.LOG_FILE):
                with open(self.LOG_FILE, "r") as f:
                    encoded_data = f.read()
                    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
                    return json.loads(decoded_data)
        except:
            pass
        return []
    
    def save_tasks(self):
        """保存任务列表为Base64编码的文件"""
        try:
            json_data = json.dumps(self.tasks)
            encoded_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
            
            with open(self.LOG_FILE, "w") as f:
                f.write(encoded_data)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存任务失败: {str(e)}")
            return False
    
    def update_task_list(self):
        """更新任务列表显示"""
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.tasks, 1):
            name = os.path.basename(task)
            self.task_list.insert(tk.END, f"{i}. {name}")
            self.task_list.itemconfig(tk.END, {'fg': '#333333'})
    
    def add_task(self):
        """添加新任务"""
        filetypes = (
            ('可执行文件', '*.exe'),
            ('批处理文件', '*.bat'),
            ('Python脚本', '*.py'),
            ('所有文件', '*.*')
        )
        
        file_path = filedialog.askopenfilename(
            title="选择要添加的任务",
            filetypes=filetypes
        )
        
        if file_path:
            if file_path not in self.tasks:
                self.tasks.append(file_path)
                if self.save_tasks():
                    self.update_task_list()
            elif file_path in self.tasks:
                pass
    
    def remove_task(self):
        """删除选中的任务"""
        selected = self.task_list.curselection()
        if not selected:
            return
        
        index = selected[0]
        self.tasks.pop(index)
        if self.save_tasks():
            self.update_task_list()
    
    def drop(self, event):
        """处理拖放事件"""
        # 正确处理带空格的路径
        file_path = event.data.strip('{}')
        
        # 检查文件扩展名
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.exe', '.bat', '.py'):
            if file_path not in self.tasks:
                self.tasks.append(file_path)
        elif ext == '.lnk':
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(file_path)
                target_path = shortcut.Targetpath
                if target_path not in self.tasks:
                    self.tasks.append(target_path)
            except:
                pass
        
        if self.save_tasks():
            self.update_task_list()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = TaskEditor(root)
    root.mainloop()
