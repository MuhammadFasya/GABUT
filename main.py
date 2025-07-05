import tkinter as tk
from tkinter import ttk, messagebox
from models.finance_manager import GamerFinanceManager
from models.expense import GamingExpense, RegularExpense
from datetime import datetime

# Impor matplotlib untuk visualisasi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GamerFinanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Finance Manager")
        self.root.geometry("1000x800") # Ukuran sedikit lebih besar
        self.root.minsize(900, 700) # Ukuran minimum
        
        self.finance_manager = GamerFinanceManager()
        
        # --- Styling ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Tema yang lebih modern
        
        # Warna Palet (inspirasi dari tema gaming/dark mode)
        self.primary_color = "#4CAF50"  # Green
        self.secondary_color = "#FFC107" # Amber
        self.accent_color = "#2196F3"    # Blue
        self.bg_dark = "#2C3E50"         # Dark Blue-Grey
        self.bg_light = "#ECF0F1"        # Light Grey
        self.text_color_dark = "#FFFFFF" # White
        self.text_color_light = "#000000" # Black

        self.style.configure('TFrame', background=self.bg_dark)
        self.style.configure('TLabel', background=self.bg_dark, foreground=self.text_color_dark, font=('Segoe UI', 10))
        self.style.configure('TButton', background=self.primary_color, foreground=self.text_color_dark, font=('Segoe UI', 10, 'bold'))
        self.style.map('TButton', 
                       background=[('active', self.primary_color)],
                       foreground=[('active', self.text_color_dark)])
        self.style.configure('TEntry', fieldbackground=self.bg_light, foreground=self.text_color_light)
        self.style.configure('TCombobox', fieldbackground=self.bg_light, foreground=self.text_color_light)
        self.style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                             background=self.bg_dark, 
                             foreground=self.text_color_dark,
                             font=('Segoe UI', 10, 'bold'), 
                             padding=[10, 5])
        self.style.map('TNotebook.Tab', 
                       background=[('selected', self.accent_color)], 
                       foreground=[('selected', self.text_color_dark)])
        self.style.configure('TLabelframe', background=self.bg_dark, foreground=self.text_color_dark)
        self.style.configure('TLabelframe.Label', background=self.bg_dark, foreground=self.accent_color, font=('Segoe UI', 11, 'bold'))
        self.style.configure('Treeview', 
                             background=self.bg_light, 
                             foreground=self.text_color_light, 
                             fieldbackground=self.bg_light,
                             font=('Segoe UI', 9))
        self.style.configure('Treeview.Heading', 
                             background=self.primary_color, 
                             foreground=self.text_color_dark, 
                             font=('Segoe UI', 10, 'bold'))
        self.style.map('Treeview.Heading', 
                       background=[('active', self.primary_color)])
        
        # Header Frame (untuk judul aplikasi)
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        app_title = ttk.Label(header_frame, text="🎮 Gamer Finance Manager 💰", 
                              font=('Impact', 24, 'bold'), 
                              foreground=self.primary_color, 
                              background=self.bg_dark)
        app_title.pack(pady=10)

        # Create main interface
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=5) # Padding lebih besar
        
        # Dashboard tab
        self.dashboard_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.dashboard_frame, text='📊 Dashboard')
        self.create_dashboard()
        
        # Add Expense tab
        self.expense_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.expense_frame, text='➕ Add Expense')
        self.create_expense_form()
        
        # Gaming Expenses tab
        self.gaming_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.gaming_frame, text='🎮 Gaming Expenses')
        self.create_gaming_expenses()
        
        # Budget Settings tab
        self.budget_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.budget_frame, text='⚙️ Budget Settings')
        self.create_budget_settings()

        # Bind tab change event to refresh data
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def on_tab_change(self, event):
        self.refresh_data() # Refresh data setiap kali tab berubah
    
    def create_dashboard(self):
        # Budget status
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="Current Budget Status", padding="15", style='TLabelframe')
        status_frame.pack(fill='x', pady=10, padx=10)
        
        self.budget_labels = {}
        labels = [
            ('Monthly Budget', 0, 0), 
            ('Gaming Budget', 0, 2), 
            ('Total Spending', 1, 0), 
            ('Gaming Spending', 1, 2), 
            ('Remaining Budget', 2, 0), 
            ('Remaining Gaming Budget', 2, 2)
        ]
        
        for label_text, row, col in labels:
            ttk.Label(status_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold')).grid(row=row, column=col, sticky='w', padx=10, pady=5)
            self.budget_labels[label_text] = ttk.Label(status_frame, text="Rp 0", font=('Arial', 11, 'bold'), foreground=self.text_color_dark)
            self.budget_labels[label_text].grid(row=row, column=col+1, sticky='w', padx=5, pady=5)
        
        # Spacer for better layout
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_columnconfigure(3, weight=1)

        # Monthly Spending Chart
        chart_frame = ttk.LabelFrame(self.dashboard_frame, text="Monthly Spending Overview", padding="10", style='TLabelframe')
        chart_frame.pack(fill='x', pady=10, padx=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 3), facecolor=self.bg_dark) # Ukuran chart
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True)

        # Recent expenses
        recent_frame = ttk.LabelFrame(self.dashboard_frame, text="Recent Expenses", padding="10", style='TLabelframe')
        recent_frame.pack(fill='both', expand=True, pady=10, padx=10)
        
        self.recent_tree = ttk.Treeview(recent_frame, columns=('Date', 'Amount', 'Description', 'Category'), show='headings', height=10)
        self.recent_tree.heading('Date', text='Date', anchor=tk.W)
        self.recent_tree.heading('Amount', text='Amount', anchor=tk.W)
        self.recent_tree.heading('Description', text='Description', anchor=tk.W)
        self.recent_tree.heading('Category', text='Category', anchor=tk.W)
        
        self.recent_tree.column('Date', width=120, anchor=tk.W)
        self.recent_tree.column('Amount', width=100, anchor=tk.E) # Align right for numbers
        self.recent_tree.column('Description', width=250, anchor=tk.W)
        self.recent_tree.column('Category', width=150, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recent_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def create_expense_form(self):
        # Regular expense form
        regular_frame = ttk.LabelFrame(self.expense_frame, text="Add Regular Expense", padding="15", style='TLabelframe')
        regular_frame.pack(fill='x', pady=10, padx=10)
        
        # Inisialisasi Entry dan Combobox secara langsung
        ttk.Label(regular_frame, text="Amount:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.regular_amount = ttk.Entry(regular_frame, width=40)
        self.regular_amount.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(regular_frame, text="Description:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.regular_desc = ttk.Entry(regular_frame, width=40)
        self.regular_desc.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(regular_frame, text="Category:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.regular_category = ttk.Combobox(regular_frame, 
                                             values=['Food', 'Transportation', 'Entertainment', 'Utilities', 'Other'],
                                             state='readonly')
        self.regular_category.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        self.regular_category.set('Food') # Default value
        
        ttk.Button(regular_frame, text="💰 Add Regular Expense", command=self.add_regular_expense, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=15)
        regular_frame.grid_columnconfigure(1, weight=1) # Agar entry meluas

        # Gaming expense form
        gaming_frame = ttk.LabelFrame(self.expense_frame, text="Add Gaming Expense", padding="15", style='TLabelframe')
        gaming_frame.pack(fill='x', pady=10, padx=10)
        
        # Inisialisasi Entry dan Combobox secara langsung untuk gaming expense
        ttk.Label(gaming_frame, text="Amount:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.gaming_amount = ttk.Entry(gaming_frame, width=40)
        self.gaming_amount.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(gaming_frame, text="Description:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.gaming_desc = ttk.Entry(gaming_frame, width=40)
        self.gaming_desc.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(gaming_frame, text="Game Title:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.game_title = ttk.Entry(gaming_frame, width=40)
        self.game_title.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(gaming_frame, text="Expense Type:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.expense_type = ttk.Combobox(gaming_frame, 
                                         values=['Game Purchase', 'DLC', 'Microtransaction', 'Hardware', 'Subscription', 'Other Gaming'],
                                         state='readonly')
        self.expense_type.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        self.expense_type.set('Game Purchase') # Default value
        
        ttk.Button(gaming_frame, text="🎮 Add Gaming Expense", command=self.add_gaming_expense, cursor="hand2").grid(row=4, column=0, columnspan=2, pady=15)
        gaming_frame.grid_columnconfigure(1, weight=1) # Agar entry meluas
        
    def create_gaming_expenses(self):
        # Gaming expenses overview
        overview_frame = ttk.LabelFrame(self.gaming_frame, text="Spending by Game", padding="10", style='TLabelframe')
        overview_frame.pack(fill='x', pady=10, padx=10)
        
        self.game_spending_text = tk.Text(overview_frame, height=8, width=50, 
                                          background=self.bg_light, foreground=self.text_color_light, 
                                          font=('Consolas', 10), relief='flat', bd=0)
        self.game_spending_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Gaming expenses list
        list_frame = ttk.LabelFrame(self.gaming_frame, text="Detailed Gaming Expenses", padding="10", style='TLabelframe')
        list_frame.pack(fill='both', expand=True, pady=10, padx=10)
        
        self.gaming_tree = ttk.Treeview(list_frame, columns=('Date', 'Amount', 'Game', 'Type', 'Description'), show='headings', height=12)
        self.gaming_tree.heading('Date', text='Date', anchor=tk.W)
        self.gaming_tree.heading('Amount', text='Amount', anchor=tk.W)
        self.gaming_tree.heading('Game', text='Game', anchor=tk.W)
        self.gaming_tree.heading('Type', text='Type', anchor=tk.W)
        self.gaming_tree.heading('Description', text='Description', anchor=tk.W)
        
        self.gaming_tree.column('Date', width=120, anchor=tk.W)
        self.gaming_tree.column('Amount', width=90, anchor=tk.E)
        self.gaming_tree.column('Game', width=180, anchor=tk.W)
        self.gaming_tree.column('Type', width=120, anchor=tk.W)
        self.gaming_tree.column('Description', width=250, anchor=tk.W)
        
        scrollbar2 = ttk.Scrollbar(list_frame, orient='vertical', command=self.gaming_tree.yview)
        self.gaming_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.gaming_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
    def create_budget_settings(self):
        settings_frame = ttk.LabelFrame(self.budget_frame, text="Set Your Budgets", padding="20", style='TLabelframe')
        settings_frame.pack(fill='x', pady=20, padx=20)
        
        ttk.Label(settings_frame, text="Monthly Budget (Rp):").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.monthly_budget_entry = ttk.Entry(settings_frame, width=30)
        self.monthly_budget_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        ttk.Label(settings_frame, text="Gaming Budget (Rp):").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.gaming_budget_entry = ttk.Entry(settings_frame, width=30)
        self.gaming_budget_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        ttk.Button(settings_frame, text="💾 Save Budget Settings", command=self.save_budget_settings, cursor="hand2").grid(row=2, column=0, columnspan=2, pady=25)
        settings_frame.grid_columnconfigure(1, weight=1)

        # Load current values
        self.monthly_budget_entry.insert(0, f"{self.finance_manager.monthly_budget:,.0f}")
        self.gaming_budget_entry.insert(0, f"{self.finance_manager.gaming_budget:,.0f}")
    
    def add_regular_expense(self):
        try:
            amount_str = self.regular_amount.get().replace('.', '').replace(',', '') # Hapus pemisah ribuan
            amount = float(amount_str)
            description = self.regular_desc.get().strip()
            category = self.regular_category.get().strip()
            
            if not description or not category or amount <= 0:
                messagebox.showerror("Input Error", "Please ensure all fields are filled correctly and amount is positive.")
                return
            
            self.finance_manager.add_expense(amount, description, category)
            messagebox.showinfo("Success", "✅ Regular expense added successfully!")
            
            # Clear form
            self.regular_amount.delete(0, tk.END)
            self.regular_desc.delete(0, tk.END)
            self.regular_category.set('Food') # Reset to default
            
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric amount for regular expense.")
    
    def add_gaming_expense(self):
        try:
            amount_str = self.gaming_amount.get().replace('.', '').replace(',', '')
            amount = float(amount_str)
            description = self.gaming_desc.get().strip()
            game_title = self.game_title.get().strip()
            expense_type = self.expense_type.get().strip()
            
            if not description or not game_title or not expense_type or amount <= 0:
                messagebox.showerror("Input Error", "Please ensure all fields are filled correctly and amount is positive.")
                return
            
            self.finance_manager.add_gaming_expense(amount, description, game_title, expense_type)
            messagebox.showinfo("Success", "🎮 Gaming expense added successfully!")
            
            # Clear form
            self.gaming_amount.delete(0, tk.END)
            self.gaming_desc.delete(0, tk.END)
            self.game_title.delete(0, tk.END)
            self.expense_type.set('Game Purchase') # Reset to default
            
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric amount for gaming expense.")
    
    def save_budget_settings(self):
        try:
            monthly_budget_str = self.monthly_budget_entry.get().replace('.', '').replace(',', '')
            gaming_budget_str = self.gaming_budget_entry.get().replace('.', '').replace(',', '')

            monthly_budget = float(monthly_budget_str)
            gaming_budget = float(gaming_budget_str)
            
            if monthly_budget < 0 or gaming_budget < 0:
                messagebox.showerror("Input Error", "Budgets cannot be negative.")
                return

            self.finance_manager.set_budgets(monthly_budget, gaming_budget)
            messagebox.showinfo("Success", "💾 Budget settings saved!")
            
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric budget amounts.")
    
    def refresh_data(self):
        # Update dashboard
        budget_status = self.finance_manager.get_budget_status()
        
        self.budget_labels['Monthly Budget'].config(text=f"Rp {budget_status['monthly_budget']:,.0f}", font=('Arial', 11, 'bold'))
        self.budget_labels['Gaming Budget'].config(text=f"Rp {budget_status['gaming_budget']:,.0f}", font=('Arial', 11, 'bold'))
        self.budget_labels['Total Spending'].config(text=f"Rp {budget_status['total_spending']:,.0f}", font=('Arial', 11, 'bold'))
        self.budget_labels['Gaming Spending'].config(text=f"Rp {budget_status['gaming_spending']:,.0f}", font=('Arial', 11, 'bold'))
        
        # Color coding for remaining budgets
        remaining_budget = budget_status['remaining_budget']
        remaining_gaming = budget_status['remaining_gaming_budget']
        
        self.budget_labels['Remaining Budget'].config(
            text=f"Rp {remaining_budget:,.0f}",
            foreground='red' if remaining_budget < 0 else (self.primary_color if remaining_budget > 0 else 'gray')
        )
        self.budget_labels['Remaining Gaming Budget'].config(
            text=f"Rp {remaining_gaming:,.0f}",
            foreground='red' if remaining_gaming < 0 else (self.primary_color if remaining_gaming > 0 else 'gray')
        )
        
        # Update recent expenses
        self.recent_tree.delete(*self.recent_tree.get_children())
        # Sort expenses by date and time to show the latest first
        sorted_expenses = sorted(self.finance_manager.expenses, key=lambda x: datetime.strptime(x.date, '%Y-%m-%d %H:%M:%S'), reverse=True)
        for expense in sorted_expenses[:20]: # Tampilkan 20 transaksi terbaru
            self.recent_tree.insert('', 'end', values=(
                expense.date.split()[0], # Hanya tanggal
                f"Rp {expense.amount:,.0f}",
                expense.description,
                expense.category.replace('_', ' ').title() # Format category lebih baik
            ))
        
        # Update gaming expenses
        self.gaming_tree.delete(*self.gaming_tree.get_children())
        sorted_gaming_expenses = sorted([e for e in self.finance_manager.expenses if isinstance(e, GamingExpense)], 
                                        key=lambda x: datetime.strptime(x.date, '%Y-%m-%d %H:%M:%S'), reverse=True)
        for expense in sorted_gaming_expenses:
            self.gaming_tree.insert('', 'end', values=(
                expense.date.split()[0],
                f"Rp {expense.amount:,.0f}",
                expense.game_title,
                expense.expense_type.replace('_', ' ').title(),
                expense.description
            ))
        
        # Update game spending overview
        self.game_spending_text.delete(1.0, tk.END)
        game_spending = self.finance_manager.get_spending_by_game()
        if game_spending:
            self.game_spending_text.insert(tk.END, "🎮 SPENDING BY GAME:\n\n")
            for game, amount in sorted(game_spending.items(), key=lambda x: x[1], reverse=True):
                self.game_spending_text.insert(tk.END, f"• {game}: Rp {amount:,.0f}\n")
        else:
            self.game_spending_text.insert(tk.END, "No gaming expenses recorded yet. Start tracking your gaming budget!\n")

        # Update Monthly Spending Chart
        self.update_spending_chart()

    def update_spending_chart(self):
        self.ax.clear() # Clear previous plot
        
        monthly_spending = self.finance_manager.get_monthly_spending()
        categories = ['Gaming', 'Other']
        amounts = [monthly_spending['gaming'], monthly_spending['other']]
        
        # Customize chart
        self.ax.bar(categories, amounts, color=[self.accent_color, self.secondary_color])
        self.ax.set_title('Current Month Spending', color=self.text_color_dark)
        self.ax.set_ylabel('Amount (Rp)', color=self.text_color_dark)
        
        # Set background and text colors for chart elements
        self.fig.set_facecolor(self.bg_dark)
        self.ax.set_facecolor(self.bg_dark)
        self.ax.tick_params(axis='x', colors=self.text_color_dark)
        self.ax.tick_params(axis='y', colors=self.text_color_dark)
        self.ax.spines['bottom'].set_color(self.text_color_dark)
        self.ax.spines['left'].set_color(self.text_color_dark)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        # Add values on top of bars
        for i, v in enumerate(amounts):
            self.ax.text(i, v + 0.01 * sum(amounts), f"Rp {v:,.0f}", ha='center', va='bottom', color=self.text_color_dark)

        self.fig.tight_layout() # Adjust layout
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = GamerFinanceGUI(root)
    root.mainloop()