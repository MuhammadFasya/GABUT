# models/expense.py
from .transaction import Transaction
from typing import Dict, Any

class GamingExpense(Transaction):
    """Gaming expense class - inheritance dari Transaction"""
    
    def __init__(self, amount: float, description: str, game_title: str, expense_type: str, date: str = None):
        super().__init__(amount, description, date)
        self.game_title = game_title
        self.expense_type = expense_type  # 'game_purchase', 'dlc', 'microtransaction', 'hardware', 'subscription'
        self.category = 'gaming'
    
    def to_dict(self) -> Dict[str, Any]:
        """Override method dari parent class"""
        data = super().to_dict()
        data.update({
            'game_title': self.game_title,
            'expense_type': self.expense_type,
            'category': self.category
        })
        return data
    
    def __str__(self):
        return f"Gaming Expense: {self.game_title} - {self.description} - Rp {self.amount:,.0f} ({self.expense_type})"

class RegularExpense(Transaction):
    """Regular expense class - inheritance dari Transaction"""
    
    def __init__(self, amount: float, description: str, category: str, date: str = None):
        super().__init__(amount, description, date)
        self.category = category
    
    def to_dict(self) -> Dict[str, Any]:
        """Override method dari parent class"""
        data = super().to_dict()
        data.update({
            'category': self.category
        })
        return data
    
    def __str__(self):
        return f"Regular Expense: {self.description} - Rp {self.amount:,.0f} ({self.category})"