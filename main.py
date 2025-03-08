import tkinter as tk
from gui.toolbar import Toolbar
from gui.components import ComponentPanel
from gui.analysis import AnalysisPanel
from gui.canvas import CircuitCanvas
from utils.file_io import FileIOHandler
from utils.helpers import show_about

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("ourCircuit")
        self.root.geometry("1200x800")

        self.components = []
        self.wires = []
        self.current_component = None

        self.file_io_handler = FileIOHandler(self, self.root) # Pass root and self for canvas access later
        self.circuit_canvas = CircuitCanvas(self, root) # Pass root and self for component management
        self.toolbar = Toolbar(self, root)
        self.component_panel = ComponentPanel(self, root)
        self.analysis_panel = AnalysisPanel(self, root)

        self.create_menu()
        self.toolbar.create_toolbar()
        self.component_panel.create_component_panel()
        self.circuit_canvas.create_canvas()
        self.analysis_panel.create_analysis_panel()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.file_io_handler.new_project)
        file_menu.add_command(label="打开", command=self.file_io_handler.open_project)
        file_menu.add_command(label="保存", command=self.file_io_handler.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=lambda: show_about())
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

    def select_component(self, component_name):
        self.current_component = component_name

    def place_component(self, x, y):
        if self.current_component:
            self.circuit_canvas.draw_component(x, y, self.current_component)
            self.create_component_instance(x, y, self.current_component)

    def create_component_instance(self, x, y, component_type_name):
        self.circuit_canvas.create_component_instance(x, y, component_type_name)

    def run_analysis(self, method):
        # Placeholder for analysis execution
        print(f"Running analysis: {method}")

    # Methods to be called by submodules to interact with main app's data if needed.
    def get_components(self):
        return self.components

    def get_wires(self):
        return self.wires

    def set_components(self, components):
        self.components = components

    def set_wires(self, wires):
        self.wires = wires

if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()