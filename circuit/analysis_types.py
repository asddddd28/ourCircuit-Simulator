# circuit/analysis_types.py
class AnalysisType:
    DC_ANALYSIS = "直流分析"
    AC_ANALYSIS = "交流分析"
    TRANSIENT_ANALYSIS = "瞬态分析"
    SINUSOIDAL_STEADY_STATE_ANALYSIS = "正弦稳态分析"
    CIRCUIT_THEOREMS = "电路定理" # e.g., Thevenin, Norton, Superposition
    LARGE_SIGNAL_ANALYSIS = "大信号分析"
    SMALL_SIGNAL_ANALYSIS = "小信号分析"
    SWITCHING_CIRCUIT_ANALYSIS = "开关电路分析"

    ALL_ANALYSIS_TYPES = [
        DC_ANALYSIS,
        AC_ANALYSIS,
        TRANSIENT_ANALYSIS,
        SINUSOIDAL_STEADY_STATE_ANALYSIS,
        CIRCUIT_THEOREMS,
        LARGE_SIGNAL_ANALYSIS,
        SMALL_SIGNAL_ANALYSIS,
        SWITCHING_CIRCUIT_ANALYSIS,
    ]