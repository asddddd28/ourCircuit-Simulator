# gui/canvas.py
import tkinter as tk
from tkinter import ttk
from circuit.elements import * # Import element classes

class CircuitCanvas:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root
        self.canvas = None
        self.component_counter = {} # To generate unique component names
        self.wire_start_point = None  # 新增导线起点状态

    def create_canvas(self):
        center_frame = ttk.Frame(self.root)
        center_frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(center_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.wire_start = None

        # 画布事件绑定
        self.canvas.bind("<Button-1>", self.place_component_event)
        self.canvas.bind("<B1-Motion>", self.draw_wire_event)
        self.canvas.bind("<ButtonRelease-1>", self.finish_wire_event)

    def place_component_event(self, event):
        if self.parent.current_component == "导线":
            if not self.wire_start_point:
                # 第一次点击记录起点
                self.wire_start_point = (event.x, event.y)
                # 在起点处绘制临时标记
                self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, 
                                      fill='blue', tags='wire_temp')
            else:
                # 第二次点击完成连线
                end_point = (event.x, event.y)
                self.canvas.create_line(self.wire_start_point, end_point, 
                                       fill="black", width=2)
                self.parent.wires.append({
                    "start": self.wire_start_point,
                    "end": end_point
                })
                # 清除临时标记并重置状态
                self.canvas.delete('wire_temp')
                self.wire_start_point = None
        else:
            # 原有元件放置逻辑保持不变
            component_type_name = self.parent.current_component
            if component_type_name:
                x, y = event.x, event.y
                self.draw_component(x, y, component_type_name)
                self.create_component_instance(x, y, component_type_name)

    # 移除原有的 draw_wire_event 和 finish_wire_event 方法

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
        
        elif component_type == "电感":
            # 绘制电感符号（波浪线圈）
            for i in range(5):
                self.canvas.create_arc(
                    x-25 + i*10, y-8, 
                    x-15 + i*10, y+8,
                    start=0, extent=-180, 
                    outline="purple"
                )
            self.canvas.create_text(x, y, text="L")
        
        elif component_type == "三极管(NMOS)":
            # 绘制NMOS晶体管符号
            self.canvas.create_rectangle(x-15, y-20, x+15, y+20, outline="black")
            # 源极(S)、漏极(D)、栅极(G)
            self.canvas.create_line(x-15, y, x-25, y)  # 源极
            self.canvas.create_line(x+15, y, x+25, y)  # 漏极
            self.canvas.create_line(x, y-20, x, y-30)  # 栅极
            self.canvas.create_line(x-5, y+15, x+5, y+15)  # 衬底箭头
        
        elif component_type == "三极管(PMOS)":
            # 绘制PMOS晶体管符号（与NMOS类似但衬底箭头方向不同）
            self.canvas.create_rectangle(x-15, y-20, x+15, y+20, outline="black")
            self.canvas.create_line(x-15, y, x-25, y)  # 源极
            self.canvas.create_line(x+15, y, x+25, y)  # 漏极
            self.canvas.create_line(x, y-20, x, y-30)  # 栅极
            self.canvas.create_line(x-5, y+15, x+5, y+15, arrow=tk.LAST)  # 衬底箭头
        
        elif component_type == "NPNBJT":
            # 绘制NPN双极晶体管
            self.canvas.create_polygon([x, y-20, x-15, y+20, x+15, y+20], outline="black")
            self.canvas.create_line(x, y-30, x, y-20)  # 基极
            self.canvas.create_line(x-15, y+20, x-25, y+25)  # 发射极
            self.canvas.create_line(x+15, y+20, x+25, y+25)  # 集电极
            self.canvas.create_line(x+5, y+18, x+10, y+22, arrow=tk.LAST)  # 箭头指示
        
        elif component_type == "集成运放":
            # 绘制运算放大器符号
            self.canvas.create_polygon([x, y-25, x-25, y, x, y+25], outline="black")  # 三角形主体
            self.canvas.create_line(x-35, y-10, x-25, y-10)  # 反相输入(-)
            self.canvas.create_line(x-35, y+10, x-25, y+10)  # 同相输入(+)
            self.canvas.create_line(x+25, y, x+35, y)  # 输出端
            self.canvas.create_text(x-20, y-12, text="-")
            self.canvas.create_text(x-20, y+12, text="+")
        
        elif component_type in ["交流电压源", "交流电流源"]:
            # 绘制交流符号（波浪线）
            for i in range(3):
                self.canvas.create_arc(
                    x-15 + i*10, y-5, 
                    x-5 + i*10, y+5,
                    start=0, extent=180, 
                    outline="orange" if "电压" in component_type else "cyan"
                )
            if component_type == "交流电压源":
                self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="orange")
                self.canvas.create_text(x, y, text="V~")
            else:
                self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="cyan")
                self.canvas.create_line(x-10, y, x+10, y, arrow=tk.LAST, fill="cyan")
                self.canvas.create_text(x, y, text="I~")
        
        elif component_type in ["开关(开)", "开关(关)"]:
            # 绘制开关符号
            self.canvas.create_line(x-15, y-15, x+15, y+15, fill="gray")
            if component_type == "开关(开)":
                self.canvas.create_line(x-15, y+15, x+15, y-15, fill="gray", dash=(4,2))
            else:  # 闭合状态
                self.canvas.create_line(x-15, y+15, x+15, y-15, fill="black")
        
        elif component_type == "结点":
            # 绘制连接结点（小圆点）
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")


    def draw_wire_event(self, event):
        # 连线绘制逻辑（简化示例）
        self.wire_start = None # Re-initialize at the start of each draw event
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
                           self.component_counter[comp_type_name] = int(comp_data['name'][1:]) if comp_data['name'][1:].isdigit() else 0

        if data and "wires" in data:
            for wire_data in data["wires"]:
                if "start" in wire_data and "end" in wire_data:
                    self.canvas.create_line(wire_data["start"], wire_data["end"], fill="black")
