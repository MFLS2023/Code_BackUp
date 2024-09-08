# -*- coding: utf-8 -*-
"""
模块: qubo

功能: 提供一系列针对QUBO的前处理工具
"""

from kaiwu.qubo._qubo_expression import binary, spin, constraint, placeholder
from kaiwu.qubo._qubo_expression import Binary, Integer, Placeholder
from kaiwu.qubo._interface import quicksum, bisection, details
from kaiwu.qubo._matrix import ndarray
from kaiwu.qubo._get_val import get_sol_dict, get_val, get_array_val
from kaiwu.qubo._convert import make, cim_ising_model
from kaiwu.qubo._convert import ising_matrix_to_qubo_matrix, qubo_matrix_to_ising_matrix
from kaiwu.qubo._convert import qubo_model_to_qubo_matrix, qubo_matrix_to_qubo_model
from kaiwu.qubo._precision import check_qubo_matrix_bit_width, adjust_qubo_matrix_precision

__all__ = [
    "binary", "spin", "constraint", "placeholder",
    "Binary", "Integer", "Placeholder",
    "quicksum", "bisection", "details",
    "ndarray",
    "get_sol_dict", "get_val", "get_array_val",
    "make", "cim_ising_model",
    "ising_matrix_to_qubo_matrix", "qubo_matrix_to_ising_matrix",
    "qubo_model_to_qubo_matrix", "qubo_matrix_to_qubo_model",
    "check_qubo_matrix_bit_width", "adjust_qubo_matrix_precision"
]
