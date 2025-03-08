import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        tools = ["新建", "打开", "保存"] # Removed toolbar_action and moved to FileIOHandler
        file_io_handler = self.parent.file_io_handler # Access FileIOHandler from parent
        tool_commands = {
            "新建": file_io_handler.new_project,
            "打开": file_io_handler.open_project,
            "保存": file_io_handler.save_project,
        }
        for tool in tools:
            btn = ttk.Button(toolbar, text=tool, command=tool_commands[tool])
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    # toolbar_action moved to file_io_handler.py