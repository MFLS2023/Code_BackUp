# -*- coding: utf-8 -*-
"""
模块: cim

功能: 提供一系列CIM求解器
"""
from kaiwu.cim._simulation_solver import SimulatedCIMOptimizer
from kaiwu.cim._simulation_solver import simulator, simulator_core, normalizer
from kaiwu.cim._precision import calculate_ising_matrix_bit_width, adjust_ising_matrix_precision

__all__ = [
    "SimulatedCIMOptimizer",
    "simulator", "simulator_core", "normalizer",
    "calculate_ising_matrix_bit_width", "adjust_ising_matrix_precision"
]
