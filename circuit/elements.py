# circuit/elements.py
class CircuitElement:
    def __init__(self, name, value=None, nodes=None, properties=None):
        self.name = name
        self.value = value  # Numerical value (e.g., resistance, capacitance, voltage)
        self.nodes = nodes if nodes is not None else [] # List of connected node names/IDs
        self.properties = properties if properties is not None else {} # Dictionary for other properties

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, value={self.value}, nodes={self.nodes})"

class Resistor(CircuitElement):
    def __init__(self, name, resistance, nodes):
        super().__init__(name, resistance, nodes)

class Capacitor(CircuitElement):
    def __init__(self, name, capacitance, nodes):
        super().__init__(name, capacitance, nodes)

class Inductor(CircuitElement):
    def __init__(self, name, inductance, nodes):
        super().__init__(name, inductance, nodes)

class Diode(CircuitElement): # Simple Diode - can be extended with models later
    def __init__(self, name, nodes):
        super().__init__(name, nodes)

class TransistorNMOS(CircuitElement): # Simple NMOS - can be extended with models later
    def __init__(self, name, nodes): # nodes: [drain, gate, source]
        super().__init__(name, nodes)

class TransistorPMOS(CircuitElement): # Simple PMOS - can be extended with models later
    def __init__(self, name, nodes): # nodes: [drain, gate, source]
        super().__init__(name, nodes)

class TransistorNPNBJT(CircuitElement): # Simple NPN BJT
    def __init__(self, name, nodes): # nodes: [collector, base, emitter]
        super().__init__(name, nodes)

class TransistorPNPBJT(CircuitElement): # Simple PNP BJT
    def __init__(self, name, nodes): # nodes: [collector, base, emitter]
        super().__init__(name, nodes)

class OpAmp(CircuitElement): # Ideal OpAmp - can be extended later
    def __init__(self, name, nodes): # nodes: [output, non_inverting_input, inverting_input]
        super().__init__(name, nodes)

class SwitchSPST(CircuitElement): # Single Pole Single Throw Switch (SPST)
    def __init__(self, name, initial_state, nodes): # initial_state: 'open' or 'closed'
        super().__init__(name, properties={'state': initial_state}, nodes=nodes)

class VoltageSourceDC(CircuitElement):
    def __init__(self, name, voltage, nodes): # nodes: [positive, negative]
        super().__init__(name, voltage, nodes)

class CurrentSourceDC(CircuitElement):
    def __init__(self, name, current, nodes): # nodes: [positive, negative] - direction of current flow
        super().__init__(name, current, nodes)

class VoltageSourceAC(CircuitElement): # Basic AC Source - sinusoidal
    def __init__(self, name, amplitude, frequency, nodes):
        super().__init__(name, value=amplitude, nodes=nodes, properties={'frequency': frequency})

class CurrentSourceAC(CircuitElement): # Basic AC Source - sinusoidal
    def __init__(self, name, amplitude, frequency, nodes):
        super().__init__(name, value=amplitude, nodes=nodes, properties={'frequency': frequency})

class Wire(CircuitElement): # Represents a wire connection - no value
    def __init__(self, name, nodes):
        super().__init__(name, None, nodes)

class Ground(CircuitElement): # Ground node - often node '0'
    def __init__(self, name, node_name='0'):
        super().__init__(name, None, [node_name]) # Ground is connected to a single node

class Node(CircuitElement): # Explicit node component (can be useful for labeling)
    def __init__(self, name):
        super().__init__(name) # Nodes themselves don't have value or connections initially, connections are made via wires/components

# Example usage (for testing):
if __name__ == '__main__':
    r1 = Resistor("R1", 1000, ["N1", "N2"])
    c1 = Capacitor("C1", 1e-6, ["N2", "0"])
    v1 = VoltageSourceDC("V1", 5, ["N1", "0"])
    print(r1)
    print(c1)
    print(v1)