from abc import ABC, abstractmethod
from typing import List, Dict

class ExpenseTracker(ABC):
    """Abstract base class untuk expense tracking - implementasi polymorphism"""
    
    @abstractmethod
    def add_expense(self, amount: float, description: str, category: str) -> None:
        """Abstract method untuk menambah expense"""
        pass
    
    @abstractmethod
    def get_expenses_by_category(self, category: str) -> List[Dict]:
        """Abstract method untuk mendapatkan expenses berdasarkan kategori"""
        pass
    
    @abstractmethod
    def get_monthly_spending(self) -> Dict[str, float]:
        """Abstract method untuk mendapatkan spending bulanan"""
        pass
    
    @abstractmethod
    def save_data(self) -> None:
        """Abstract method untuk menyimpan data"""
        pass