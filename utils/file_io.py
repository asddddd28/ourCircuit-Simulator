import json
from tkinter import filedialog, messagebox

class FileIOHandler:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root

    def new_project(self):
        self.parent.circuit_canvas.clear_canvas()
        self.parent.set_components([]) # Use setter method
        self.parent.set_wires([])      # Use setter method

    def save_project(self):
        data = {
            "components": self.parent.get_components(), # Use getter method
            "wires": self.parent.get_wires()           # Use getter method
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
            self.parent.circuit_canvas.redraw_canvas(data) # Use canvas redraw
            self.parent.set_components(data["components"]) # Use setter method
            self.parent.set_wires(data["wires"])           # Use setter method