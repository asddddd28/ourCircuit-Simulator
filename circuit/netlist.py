# circuit/netlist.py
import json
from circuit.elements import * # Import element classes

class NetlistHandler:
    def __init__(self):
        pass

    def load_netlist(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                components_data = data.get('components', [])
                wires_data = data.get('wires', [])

                components = []
                for comp_data in components_data:
                    comp_type = comp_data['type']
                    comp_name = comp_data['name']
                    comp_value = comp_data.get('value')
                    comp_nodes = comp_data['nodes']
                    comp_properties = comp_data.get('properties', {})

                    element_class = globals().get(comp_type) # Dynamically get class from string name
                    if element_class:
                        component = element_class(comp_name, comp_value, comp_nodes, comp_properties) # Assuming constructor matches
                        components.append(component)
                    else:
                        print(f"Warning: Unknown component type '{comp_type}' in netlist.")

                wires = [] # Wires are currently just data, not element instances in loaded netlist
                for wire_data in wires_data:
                    wires.append(wire_data) # Just load wire data as is for now

                return components, wires

        except FileNotFoundError:
            print(f"Error: Netlist file not found: {filepath}")
            return [], [] # Return empty lists if file not found
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in netlist file: {filepath}")
            return [], []
        except Exception as e:
            print(f"Error loading netlist: {e}")
            return [], []


    def save_netlist(self, filepath, components, wires):
        component_list = []
        for comp in components:
            comp_data = {
                'type': comp.__class__.__name__, # Store class name as type
                'name': comp.name,
                'nodes': comp.nodes,
            }
            if comp.value is not None:
                comp_data['value'] = comp.value
            if comp.properties:
                comp_data['properties'] = comp.properties
            component_list.append(comp_data)

        netlist_data = {
            'components': component_list,
            'wires': wires # Save wire data as is
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(netlist_data, f, indent=4) # Indent for readability
            print(f"Netlist saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving netlist: {e}")
            return False

    def parse_netlist(self, netlist_text):
        # Placeholder for actual netlist parsing (e.g., SPICE format)
        print("Netlist parsing not implemented yet.")
        pass

# Example usage (for testing):
if __name__ == '__main__':
    netlist_handler = NetlistHandler()

    # Create some elements
    components_to_save = [
        Resistor("R1", 1000, ["N1", "N2"]),
        Capacitor("C1", 1e-6, ["N2", "0"]),
        VoltageSourceDC("V1", 5, ["N1", "0"])
    ]
    wires_to_save = [
        {"start": [100, 100], "end": [200, 100]},
        {"start": [200, 100], "end": [200, 200]}
    ]

    # Save to netlist file
    netlist_handler.save_netlist("test_netlist.cir", components_to_save, wires_to_save)

    # Load from netlist file
    loaded_components, loaded_wires = netlist_handler.load_netlist("test_netlist.cir")
    print("\nLoaded Components:")
    for comp in loaded_components:
        print(comp)
    print("\nLoaded Wires:", loaded_wires)