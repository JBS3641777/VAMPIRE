"""
K2 Driver - High-Output Circuit Financial Transaction Processor
Version: 3.0
Author: TeddyBear Financial Systems
Commitment: GDX-COMMITMENT-MEMORY-TERMINAL
"""

from .k2_core import K2Core
from .financial_engine import FinancialEngine
from .transaction_processor import TransactionProcessor
from .human_interface import HumanInterface

__version__ = "3.0.0"
__all__ = ['K2Core', 'FinancialEngine', 'TransactionProcessor', 'HumanInterface']