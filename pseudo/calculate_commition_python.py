class CommissionCalculator:
    def __init__(self, initial_amount):
        self.initial_amount = initial_amount
        self.total_pay = 0
        self.total_bill = 0
        self.running_balance = 0
        self.settled_balance = 0
        self.cumulative_settled_balance = 0
        self.pending_arrears = initial_amount
    
    def process_action(self, action, amount):
        if action == "Paid":
            self.total_pay += amount
        elif action == "Bill":
            self.total_bill += amount
        elif action == "Return":
            self.total_pay -= amount
        elif action == "Balance Transfer":
            # Handle balance transfer (custom logic based on requirement)
            self.running_balance -= amount
            self.settled_balance -= amount
        
        self.running_balance = self.total_pay - self.total_bill
        self.settled_balance = self.running_balance - self.cumulative_settled_balance
        self.cumulative_settled_balance += max(self.settled_balance, 0)  # Only add positive settlements
        self.pending_arrears = self.initial_amount - self.cumulative_settled_balance
    
    def display_status(self):
        return {
            "Total Pay": self.total_pay,
            "Total Bill": self.total_bill,
            "Running Balance": self.running_balance,
            "Settled Balance": self.settled_balance,
            "Cumulative Settled Balance": self.cumulative_settled_balance,
            "Pending Arrears": self.pending_arrears
        }

# Example Usage
actions_list = [
    ("Paid", 10000),
    ("Return", 10000),
    ("Paid", 10000),
    # ("Return", 7000),
    ("Paid", 13000),
    # ("Paid", 7000),
    ("Bill", 3000),
    # ("Paid", 6000),
    ("Paid", 10000),
    ("Bill", 2000),
    # ("Balance Transfer", 10000)
]

calculator = CommissionCalculator(35000)
for action, amount in actions_list:
    calculator.process_action(action, amount)
    print(calculator.display_status())
