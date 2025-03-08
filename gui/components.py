import tkinter as tk
from tkinter import ttk

class ComponentPanel:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root

    def create_component_panel(self):
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

        tree.bind("<<TreeviewSelect>>", self.select_component_event)
        tree.pack(expand=True, fill=tk.BOTH)

    def select_component_event(self, event):
        tree = event.widget
        try:
            item = tree.selection()[0]
            # 获取选中项的父节点（如果是分类节点则忽略）
            if tree.parent(item) == '':  # 分类节点不触发选择
                return
                
            text = tree.item(item, "text")
            # 所有有效元件列表（从分类字典自动生成）
            allowed_components = {
                '电阻', '二极管', '三极管(NMOS)', '三极管(PMOS)', 'NPNBJT', 'PNPBJT',
                '集成运放', '电容', '电感', '开关(开)', '开关(关)', '直流电压源',
                '直流电流源', '交流电压源', '交流电流源', '导线', '地', '结点'
            }
            
            if text in allowed_components:
                self.parent.select_component(text)
        except (IndexError, KeyError):
            return  # 处理空选择或无效节点的情况