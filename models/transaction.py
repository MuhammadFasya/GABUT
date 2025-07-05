from datetime import datetime
from typing import Dict, Any

class Transaction:
    """Base class untuk semua transaksi"""
    
    def __init__(self, amount: float, description: str, date: str = None):
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = f"{self.date}_{hash(description)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for JSON storage"""
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date
        }
    
    def __str__(self):
        return f"Transaction: {self.description} - Rp {self.amount:,.0f} on {self.date}"