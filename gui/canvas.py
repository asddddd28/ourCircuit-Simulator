# gui/canvas.py
import tkinter as tk
from tkinter import ttk
from circuit.elements import * # Import element classes

class CircuitCanvas:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root
        self.canvas = None
        self.wire_start = None
        self.component_counter = {} # To generate unique component names

    def create_canvas(self):
        center_frame = ttk.Frame(self.root)
        center_frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(center_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 画布事件绑定
        self.canvas.bind("<Button-1>", self.place_component_event)
        self.canvas.bind("<B1-Motion>", self.draw_wire_event)
        self.canvas.bind("<ButtonRelease-1>", self.finish_wire_event)

    def place_component_event(self, event):
        component_type_name = self.parent.current_component # Get component type name string
        if component_type_name:
            x, y = event.x, event.y
            self.draw_component(x, y, component_type_name)
            self.create_component_instance(x, y, component_type_name) # Create element instance

    def get_unique_component_name(self, component_type_name):
        if component_type_name not in self.component_counter:
            self.component_counter[component_type_name] = 1
        else:
            self.component_counter[component_type_name] += 1
        return f"{component_type_name[0].upper()}{self.component_counter[component_type_name]}" # e.g., R1, C2, V3...

    def create_component_instance(self, x, y, component_type_name):
        component_name = self.get_unique_component_name(component_type_name)
        nodes = [] # Nodes will be connected later via wires/node placement
        component_instance = None

        if component_type_name == "电阻":
            component_instance = Resistor(component_name, 1000, nodes) # Default 1kOhm
        elif component_type_name == "电容":
            component_instance = Capacitor(component_name, 1e-6, nodes) # Default 1uF
        elif component_type_name == "二极管":
            component_instance = Diode(component_name, nodes)
        elif component_type_name == "导线":
            pass # Wires are handled differently, no instance created directly upon "placement"
        elif component_type_name == "直流电压源":
            component_instance = VoltageSourceDC(component_name, 5, nodes) # Default 5V
        elif component_type_name == "直流电流源":
            component_instance = CurrentSourceDC(component_name, 0.001, nodes) # Default 1mA
        elif component_type_name == "地":
            component_instance = Ground(component_name)
            self.parent.components.append(component_instance) # Ground is a special component, add immediately
            return # Ground doesn't need to be added to components list again below

        if component_instance:
            self.parent.components.append(component_instance) # Add to main app's components list
            print(f"Component '{component_name}' of type '{component_type_name}' placed at ({x}, {y})")


    def draw_component(self, x, y, component_type):
        # 绘制元件图形（简单示例）
        if component_type == "电阻":
            self.canvas.create_rectangle(x-20, y-10, x+20, y+10, fill="gray")
            self.canvas.create_text(x, y, text="R")
        elif component_type == "电容":
            self.canvas.create_rectangle(x-15, y-5, x+15, y+5, fill="blue")
            self.canvas.create_text(x, y, text="C")
        elif component_type == "二极管":
            self.canvas.create_polygon([x-15, y-10, x+15, y, x-15, y+10], fill="lightblue")
            self.canvas.create_line(x-15, y-10, x-15, y+10) # Cathode bar
            self.canvas.create_text(x, y, text="D")
        elif component_type == "导线":
            pass # Wire drawing is handled in draw_wire_event and finish_wire_event
        elif component_type == "直流电压源":
            self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="red")
            self.canvas.create_line(x-10, y, x+10, y, fill="red") # + sign
            self.canvas.create_line(x, y-10, x, y+10, fill="red") # - sign
            self.canvas.create_text(x, y, text="V")
        elif component_type == "直流电流源":
            self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="green")
            self.canvas.create_line(x-10, y, x+10, y, arrow=tk.LAST, fill="green") # Arrow for current
            self.canvas.create_text(x, y, text="I")
        elif component_type == "地":
            self.canvas.create_polygon([x-10, y+10, x+10, y+10, x, y-10], fill="brown")
            self.canvas.create_line(x-10, y+10, x+10, y+10)
            self.canvas.create_line(x-7, y+15, x+7, y+15)
            self.canvas.create_line(x-4, y+20, x+4, y+20)
            self.canvas.create_text(x, y-20, text="GND")


    def draw_wire_event(self, event):
        # 连线绘制逻辑（简化示例）
        if self.parent.current_component == "导线": # Check component selection from parent
            if not self.wire_start:
                self.wire_start = (event.x, event.y)
            else:
                self.canvas.create_line(self.wire_start, (event.x, event.y), fill="black")
                self.wire_start = (event.x, event.y)

    def finish_wire_event(self, event):
        if hasattr(self, 'wire_start') and self.parent.current_component == "导线": # Check component selection from parent
            if self.wire_start:
                wire_end = (event.x, event.y)
                self.parent.wires.append({"start": self.wire_start, "end": wire_end}) # Store wire data
                del self.wire_start


    def clear_canvas(self):
        self.canvas.delete("all")
        self.component_counter = {} # Reset component counter when clearing canvas

    def redraw_canvas(self, data):
        self.clear_canvas()
        self.component_counter = {} # Reset counter for redraw as well
        if data and "components" in data:
            for comp_data in data["components"]:
                comp_type_name = comp_data["type"]
                pos = comp_data["position"] # Assuming position was saved
                if pos:
                    self.draw_component(pos[0], pos[1], comp_type_name)
                    # Recreate component instances here if needed for simulation
                    # and add them to self.parent.components
                    element_class = globals().get(comp_type_name)
                    if element_class:
                        # Basic recreation for display, may need more robust method for loaded data
                        component_instance = element_class(comp_data['name'], comp_data.get('value'), comp_data['nodes'], comp_data.get('properties'))
                        self.parent.components.append(component_instance)
                        if comp_type_name in self.component_counter:
                           self.component_counter[comp_type_name] = max(self.component_counter[comp_type_name], int(comp_data['name'][1:]) if comp_data['name'][1:].isdigit() else 0)
                        else:
                           self.component_counter[comp_type_name] = int(comp_data['name'][1:]) if comp_data['name'][1:].isdigit() else 0

        if data and "wires" in data:
            for wire_data in data["wires"]:
                if "start" in wire_data and "end" in wire_data:
                    self.canvas.create_line(wire_data["start"], wire_data["end"], fill="black")