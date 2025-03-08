# gui/analysis.py
import tkinter as tk
from tkinter import ttk, messagebox
from circuit.solver import CircuitSolver # Import the solver
from circuit.analysis_types import AnalysisType

class AnalysisPanel:
    def __init__(self, parent, root):
        self.parent = parent # CircuitSimulator instance
        self.root = root
        self.solver = CircuitSolver() # Instantiate the solver

    def create_analysis_panel(self):
        right_panel = ttk.Frame(self.root, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        analysis = [
            (AnalysisType.DC_ANALYSIS, [AnalysisType.DC_ANALYSIS]), # Using AnalysisType constants
            (AnalysisType.CIRCUIT_THEOREMS, [AnalysisType.CIRCUIT_THEOREMS]),
            (AnalysisType.LARGE_SIGNAL_ANALYSIS, [AnalysisType.LARGE_SIGNAL_ANALYSIS, AnalysisType.SMALL_SIGNAL_ANALYSIS]),
            (AnalysisType.SWITCHING_CIRCUIT_ANALYSIS, [AnalysisType.SWITCHING_CIRCUIT_ANALYSIS]),
            (AnalysisType.SINUSOIDAL_STEADY_STATE_ANALYSIS, [AnalysisType.SINUSOIDAL_STEADY_STATE_ANALYSIS])
        ]

        for title, items in analysis:
            frame = ttk.LabelFrame(right_panel, text=title)
            for item in items:
                btn = ttk.Button(frame, text=item, command=lambda analysis_type=item: self.run_analysis_command(analysis_type)) # Pass analysis type
                btn.pack(fill=tk.X, padx=2, pady=2)
            frame.pack(fill=tk.X, padx=5, pady=2)

    def run_analysis_command(self, analysis_type):
        components = self.parent.components # Get components from main app
        if not components:
            messagebox.showwarning("Warning", "No components in the circuit to analyze.")
            return

        if analysis_type == AnalysisType.DC_ANALYSIS:
            results, currents = self.solver.solve_dc(components)
            if "error" in results:
                messagebox.showerror("DC Analysis Error", results["error"])
            else:
                result_str = "DC Analysis Results:\nNode Voltages:\n"
                for node, voltage in results.items():
                    result_str += f"Node {node}: {voltage:.3f}V\n"
                result_str += "\nBranch Currents:\n"
                for comp_name, current in currents.items():
                    result_str += f"{comp_name}: {current}\n" # Current might be "N/A" for voltage source
                messagebox.showinfo("DC Analysis Results", result_str)
        elif analysis_type == AnalysisType.AC_ANALYSIS:
            results, currents = self.solver.solve_ac(components) # Example, AC not implemented yet
            messagebox.showinfo("Analysis Result", results.get("message", "Analysis type not yet fully implemented."))
        else: # Placeholder for other analysis types
            messagebox.showinfo("Analysis Result", f"{analysis_type} analysis (Feature to be implemented).")
        self.parent.run_analysis(analysis_type) # Call parent's run_analysis method (for potential further actions)