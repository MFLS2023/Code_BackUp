# -*- coding: utf-8 -*-
"""
模块: classical

功能: 提供一系列经典求解器
"""
from kaiwu.classical._simulated_annealing import simulated_annealing, SimulatedAnnealingOptimizer
from kaiwu.classical._tabu_search import tabu_search, TabuSearchOptimizer

__all__ = [
    "simulated_annealing", "SimulatedAnnealingOptimizer",
    "tabu_search", "TabuSearchOptimizer"
]
