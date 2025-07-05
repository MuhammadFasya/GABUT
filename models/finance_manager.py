import json
import os
from datetime import datetime
from typing import List, Dict, Any
from tkinter import messagebox

from .expense_tracker import ExpenseTracker
from .transaction import Transaction
from .expense import GamingExpense, RegularExpense

class GamerFinanceManager(ExpenseTracker):
    """Main finance manager class - implements ExpenseTracker (polymorphism)"""
    
    def __init__(self, data_file: str = 'data/gamer_finance.json'):
        self.data_file = data_file
        self.expenses: List[Transaction] = []
        self.monthly_budget = 0
        self.gaming_budget = 0
        self.load_data()
    
    def load_data(self):
        """Load data dari JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.monthly_budget = data.get('monthly_budget', 0)
                    self.gaming_budget = data.get('gaming_budget', 0)
                    
                    # Load expenses
                    for expense_data in data.get('expenses', []):
                        if expense_data.get('category') == 'gaming':
                            expense = GamingExpense(
                                expense_data['amount'],
                                expense_data['description'],
                                expense_data['game_title'],
                                expense_data['expense_type'],
                                expense_data['date']
                            )
                        else:
                            expense = RegularExpense(
                                expense_data['amount'],
                                expense_data['description'],
                                expense_data['category'],
                                expense_data['date']
                            )
                        self.expenses.append(expense)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_data(self) -> None:
        """Implementation dari abstract method - menyimpan data ke JSON"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = {
            'monthly_budget': self.monthly_budget,
            'gaming_budget': self.gaming_budget,
            'expenses': [expense.to_dict() for expense in self.expenses]
        }
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def add_expense(self, amount: float, description: str, category: str) -> None:
        """Implementation dari abstract method - menambah regular expense"""
        expense = RegularExpense(amount, description, category)
        self.expenses.append(expense)
        self.save_data()
    
    def add_gaming_expense(self, amount: float, description: str, game_title: str, expense_type: str):
        """Method khusus untuk menambah gaming expense"""
        expense = GamingExpense(amount, description, game_title, expense_type)
        self.expenses.append(expense)
        self.save_data()
    
    def get_expenses_by_category(self, category: str) -> List[Dict]:
        """Implementation dari abstract method - mendapatkan expenses berdasarkan kategori"""
        return [expense.to_dict() for expense in self.expenses if expense.category == category]
    
    def get_monthly_spending(self) -> Dict[str, float]:
        """Implementation dari abstract method - mendapatkan spending bulanan"""
        current_month = datetime.now().strftime("%Y-%m")
        monthly_spending = {'gaming': 0, 'other': 0}
        
        for expense in self.expenses:
            if expense.date.startswith(current_month):
                if expense.category == 'gaming':
                    monthly_spending['gaming'] += expense.amount
                else:
                    monthly_spending['other'] += expense.amount
        
        return monthly_spending
    
    def get_spending_by_game(self) -> Dict[str, float]:
        """Method untuk mendapatkan spending berdasarkan game"""
        game_spending = {}
        for expense in self.expenses:
            if isinstance(expense, GamingExpense):
                if expense.game_title not in game_spending:
                    game_spending[expense.game_title] = 0
                game_spending[expense.game_title] += expense.amount
        return game_spending
    
    def set_budgets(self, monthly_budget: float, gaming_budget: float):
        """Method untuk mengatur budget"""
        self.monthly_budget = monthly_budget
        self.gaming_budget = gaming_budget
        self.save_data()
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Method untuk mendapatkan status budget"""
        monthly_spending = self.get_monthly_spending()
        total_spending = monthly_spending['gaming'] + monthly_spending['other']
        
        return {
            'monthly_budget': self.monthly_budget,
            'gaming_budget': self.gaming_budget,
            'total_spending': total_spending,
            'gaming_spending': monthly_spending['gaming'],
            'remaining_budget': self.monthly_budget - total_spending,
            'remaining_gaming_budget': self.gaming_budget - monthly_spending['gaming']
        }
    
    def get_expense_summary(self) -> Dict[str, Any]:
        """Method untuk mendapatkan ringkasan expenses"""
        total_expenses = len(self.expenses)
        gaming_expenses = len([e for e in self.expenses if e.category == 'gaming'])
        regular_expenses = total_expenses - gaming_expenses
        
        return {
            'total_expenses': total_expenses,
            'gaming_expenses': gaming_expenses,
            'regular_expenses': regular_expenses,
            'total_amount': sum(e.amount for e in self.expenses),
            'gaming_amount': sum(e.amount for e in self.expenses if e.category == 'gaming'),
            'regular_amount': sum(e.amount for e in self.expenses if e.category != 'gaming')
        }