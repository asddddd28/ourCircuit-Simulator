import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("电路分析软件")
        self.root.geometry("1200x800")
        
        # 电路元件存储结构
        self.components = []
        self.wires = []
        self.current_component = None
        
        self.create_menu()
        self.create_toolbar()
        self.create_left_panel()
        self.create_center_area()
        self.create_right_panel()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.new_project)
        file_menu.add_command(label="打开", command=self.open_project)
        file_menu.add_command(label="保存", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        tools = ["新建", "打开", "保存"]
        for tool in tools:
            btn = ttk.Button(toolbar, text=tool, command=lambda t=tool: self.toolbar_action(t))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
    
    def create_left_panel(self):
        left_panel = ttk.Frame(self.root, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # 元件分类树
        tree = ttk.Treeview(left_panel)
        tree.heading("#0", text="元件库", anchor=tk.W)
        
        categories = {
            "线性电阻": ["电阻"],
            "非线性电阻": ["二极管", "三极管(NMOS)", "三极管(PMOS)", "NPNBJT", "PNPBJT", "集成运放"],
            "动态元件": ["电容", "电感"],
            "开关元件": ["开关(开)", "开关(关)"],
            "电源元件": ["直流电压源", "直流电流源", "交流电压源", "交流电流源"],
            "其他": ["导线", "地", "结点"]
        }
        
        for cat, items in categories.items():
            node = tree.insert("", tk.END, text=cat)
            for item in items:
                tree.insert(node, tk.END, text=item)
        
        tree.bind("<<TreeviewSelect>>", self.select_component)
        tree.pack(expand=True, fill=tk.BOTH)
        
    def create_center_area(self):
        center_frame = ttk.Frame(self.root)
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        self.canvas = tk.Canvas(center_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # 画布事件绑定
        self.canvas.bind("<Button-1>", self.place_component)
        self.canvas.bind("<B1-Motion>", self.draw_wire)
        self.canvas.bind("<ButtonRelease-1>", self.finish_wire)
        
    def create_right_panel(self):
        right_panel = ttk.Frame(self.root, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        analysis = [
            ("直流分析", ["节点解析法"]),
            ("电路定理", ["戴维南定理", "诺顿定理", "叠加定理"]),
            ("信号分析", ["大信号分析", "小信号分析"]),
            ("动态分析", ["开关电路分析"]),
            ("稳态分析", ["正弦稳态分析"])
        ]
        
        for title, items in analysis:
            frame = ttk.LabelFrame(right_panel, text=title)
            for item in items:
                btn = ttk.Button(frame, text=item, command=lambda i=item: self.run_analysis(i))
                btn.pack(fill=tk.X, padx=2, pady=2)
            frame.pack(fill=tk.X, padx=5, pady=2)
    
    def select_component(self, event):
        tree = event.widget
        item = tree.selection()[0]
        text = tree.item(item, "text")
        if text in ["电阻", "电容", "二极管"]:  # 示例元件
            self.current_component = text
    
    def place_component(self, event):
        if self.current_component:
            x, y = event.x, event.y
            # 绘制元件图形（简单示例）
            if self.current_component == "电阻":
                self.canvas.create_rectangle(x-20, y-10, x+20, y+10, fill="gray")
                self.canvas.create_text(x, y, text="R")
            elif self.current_component == "电容":
                self.canvas.create_rectangle(x-15, y-5, x+15, y+5, fill="blue")
                self.canvas.create_text(x, y, text="C")
            # 记录元件信息
            self.components.append({
                "type": self.current_component,
                "position": (x, y),
                "properties": {}  # 可添加参数
            })
    
    def draw_wire(self, event):
        # 连线绘制逻辑（简化示例）
        if self.current_component == "导线":
            if not hasattr(self, 'wire_start'):
                self.wire_start = (event.x, event.y)
            else:
                self.canvas.create_line(self.wire_start, (event.x, event.y), fill="black")
                self.wire_start = (event.x, event.y)
    
    def finish_wire(self, event):
        if hasattr(self, 'wire_start'):
            del self.wire_start
    
    def run_analysis(self, method):
        messagebox.showinfo("分析功能", f"执行 {method} 分析（功能待实现）")
    
    def new_project(self):
        self.canvas.delete("all")
        self.components = []
        self.wires = []
    
    def save_project(self):
        data = {
            "components": self.components,
            "wires": self.wires
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".cir")
        if file_path:
            with open(file_path, "w") as f:
                json.dump(data, f)
    
    def open_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("Circuit Files", "*.cir")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
            self.redraw_canvas(data)
    
    def redraw_canvas(self, data):
        self.canvas.delete("all")
        for comp in data["components"]:
            # 根据保存的数据重新绘制元件
            pass  # 需要实现具体绘制逻辑
    
    def show_about(self):
        messagebox.showinfo("关于", "电路分析软件 v1.0\n作者: Your Name")
    
    def toolbar_action(self, tool):
        if tool == "新建":
            self.new_project()
        elif tool == "打开":
            self.open_project()
        elif tool == "保存":
            self.save_project()

if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()