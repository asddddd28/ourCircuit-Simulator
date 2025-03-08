# circuit/solver.py
import numpy as np

class CircuitSolver:
    def __init__(self):
        pass

    def solve_dc(self, components):
        """
        Performs DC analysis using nodal analysis.
        Simplified for resistors and DC voltage/current sources only.
        """
        nodes = set()
        node_components = {} # Components connected to each node

        # Collect nodes and components connected to each node
        for comp in components:
            for node in comp.nodes:
                nodes.add(node)
                if node not in node_components:
                    node_components[node] = []
                node_components[node].append(comp)

        # Remove ground node '0' from unknowns if present, use it as reference.
        if '0' in nodes:
            nodes.remove('0')
        node_list = list(nodes) # Ordered list of unknown nodes
        num_nodes = len(node_list)

        if num_nodes == 0:
            return {}, {} # No unknown nodes, trivial circuit

        # Initialize matrices for nodal analysis: G (conductance), I (current sources), V (node voltages)
        G = np.zeros((num_nodes, num_nodes))
        I = np.zeros(num_nodes)

        node_index_map = {node: i for i, node in enumerate(node_list)} # Map node name to index in matrices

        # Fill in G and I matrices
        for i, node_name in enumerate(node_list):
            for comp in node_components[node_name]:
                comp_type = type(comp)
                comp_nodes = comp.nodes

                if comp_type is Resistor:
                    resistance = comp.value
                    conductance = 1 / resistance
                    other_node = [n for n in comp_nodes if n != node_name][0] # Get the other node

                    G[i, i] += conductance # Diagonal element (sum of conductances connected to node i)
                    if other_node != '0': # If not connected to ground
                        j = node_index_map.get(other_node)
                        if j is not None:
                            G[i, j] -= conductance # Off-diagonal element (negative conductance between nodes i and j)

                elif comp_type is VoltageSourceDC:
                    voltage = comp.value
                    pos_node, neg_node = comp_nodes

                    if pos_node == node_name:
                        I[i] += voltage / 1e9 # Approximating as a large current source for voltage source (simplified nodal analysis)
                    elif neg_node == node_name:
                        I[i] -= voltage / 1e9 # Approximating as a large current source for voltage source (simplified nodal analysis)

                elif comp_type is CurrentSourceDC:
                    current = comp.value
                    pos_node, neg_node = comp_nodes # Current direction from pos_node to neg_node

                    if pos_node == node_name:
                        I[i] -= current # Current source flowing *out* of the node
                    elif neg_node == node_name:
                        I[i] += current # Current source flowing *into* the node

        try:
            # Solve the linear system GV = I for node voltages V
            V_unknown = np.linalg.solve(G, I)
            node_voltages = {'0': 0} # Ground node voltage is 0
            for i, node_name in enumerate(node_list):
                node_voltages[node_name] = V_unknown[i]

            branch_currents = {}
            for comp in components:
                if type(comp) is Resistor:
                    node1, node2 = comp.nodes
                    v1 = node_voltages.get(node1, 0) # Get node voltage, default to 0 if not found (ground)
                    v2 = node_voltages.get(node2, 0)
                    current = (v1 - v2) / comp.value # Ohm's law, current from node1 to node2
                    branch_currents[comp.name] = current
                elif type(comp) is VoltageSourceDC:
                    # For a voltage source, current calculation is more complex in nodal analysis
                    # For simplicity, we can approximate or leave it for more advanced analysis
                    branch_currents[comp.name] = "N/A (Voltage Source)"
                elif type(comp) is CurrentSourceDC:
                    branch_currents[comp.name] = comp.value # Current through current source is its defined value

            return node_voltages, branch_currents

        except np.linalg.LinAlgError:
            return {"error": "Singular matrix - Circuit may have issues (e.g., floating nodes, voltage source loop)."}, {}
        except Exception as e:
            return {"error": f"Error during DC analysis: {e}"}, {}


    def solve_ac(self, circuit_netlist):
        # Placeholder for AC analysis
        return {"message": "AC analysis not implemented yet."}, {}

    def solve_transient(self, circuit_netlist):
        # Placeholder for Transient analysis
        return {"message": "Transient analysis not implemented yet."}, {}

    def solve_sinusoidal_steady_state(self, circuit_netlist):
        # Placeholder for Sinusoidal Steady State analysis
        return {"message": "Sinusoidal Steady State analysis not implemented yet."}, {}


# Example usage (for testing):
if __name__ == '__main__':
    solver = CircuitSolver()

    # Simple voltage divider circuit
    components_example = [
        Resistor("R1", 1000, ["N1", "N2"]),
        Resistor("R2", 2000, ["N2", "0"]),
        VoltageSourceDC("V1", 9, ["N1", "0"])
    ]

    node_voltages, branch_currents = solver.solve_dc(components_example)
    print("DC Analysis Results:")
    print("Node Voltages:", node_voltages)
    print("Branch Currents:", branch_currents)

    # Example with a current source
    components_example_current_source = [
        Resistor("R3", 500, ["N3", "0"]),
        CurrentSourceDC("I1", 0.01, ["N3", "0"]) # 10mA source into node N3
    ]
    node_voltages_cs, branch_currents_cs = solver.solve_dc(components_example_current_source)
    print("\nDC Analysis with Current Source:")
    print("Node Voltages:", node_voltages_cs)
    print("Branch Currents:", branch_currents_cs)

    # Example with error case (floating node - R only connected to one node, except ground)
    components_error_example = [
        Resistor("R4", 1000, ["N4", "0"]), # R connected to ground and N4
        Resistor("R5", 2000, ["N5", "N4"]), # R connected to N4 and N5, N5 floating (except ground)
        VoltageSourceDC("V2", 5, ["N4", "0"])
    ]
    node_voltages_err, branch_currents_err = solver.solve_dc(components_error_example)
    print("\nDC Analysis Error Example:")
    print("Node Voltages:", node_voltages_err)
    print("Branch Currents:", branch_currents_err)