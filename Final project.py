import tkinter as tk
from tkinter import messagebox

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: £{self.price:.2f}"

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        for _ in range(quantity):
            self.items.append(item)

    def total_cost(self):
        return sum(item.price for item in self.items)

    def prioritized_items(self):
        priority_items = [item for item in self.items if item.name in ["Fresh Caught Lobster", "Steak Diane"]]
        other_items = [item for item in self.items if item.name not in ["Fresh Caught Lobster", "Steak Diane"]]
        return priority_items + other_items

    def __str__(self):
        return "\n".join([str(item) for item in self.items])

class Table:
    def __init__(self, table_id):
        self.table_id = table_id
        self.booked_sessions = {"early": False, "late": False}
        self.orders = {"early": Order(), "late": Order()}
        self.diners = {"early": 0, "late": 0}
        self.tips = {"early": 0, "late": 0}

    def book(self, session):
        if session not in self.booked_sessions:
            raise ValueError("Invalid session. Use 'early' or 'late'.")
        if not self.booked_sessions[session]:
            self.booked_sessions[session] = True
            return True
        raise ValueError(f"Table {self.table_id} is already booked for the {session} session.")

    def add_order(self, session, item, quantity=1, diners=1):
        if session not in self.booked_sessions:
            raise ValueError("Invalid session. Use 'early' or 'late'.")
        if not self.booked_sessions[session]:
            raise ValueError("Session not booked.")
        if self.diners[session] + diners > 8:
            raise ValueError("Exceeds table capacity of 8 diners")
        self.diners[session] += diners
        self.orders[session].add_item(item, quantity)

    def calculate_bill(self, session, payment_method='cash', tip=0):
        if session not in self.booked_sessions:
            raise ValueError("Invalid session. Use 'early' or 'late'.")
        total_cost = self.orders[session].total_cost()
        if payment_method == 'credit card':
            total_cost *= 1.10
        total_cost += tip
        self.tips[session] = tip  # Record the tip for reporting
        return total_cost

    def __str__(self):
        return f"Table {self.table_id}"

class Restaurant:
    def __init__(self):
        self.tables = [Table(i) for i in range(1, 6)]
        self.menu = self.load_menu()

    def load_menu(self):
        # Load the menu dynamically
        return {
            "House Cured Bourbon Gravadlax": MenuItem("House Cured Bourbon Gravadlax", 9.99),
            "Bloc de Pate": MenuItem("Bloc de Pate", 14.99),
            "Village Market Tasting Plate": MenuItem("Village Market Tasting Plate", 7.99),
            "White's Out Seafood Cocktail": MenuItem("White's Out Seafood Cocktail", 14.99),
            "Twist Baked Essex Camembert Soufflé": MenuItem("Twist Baked Essex Camembert Soufflé", 9.99),
            "28 Day Aged rib of Beef": MenuItem("28 Day Aged rib of Beef", 45.99),
            "Steak Diane": MenuItem("Steak Diane", 49.99),
            "Fresh Caught Lobster": MenuItem("Fresh Caught Lobster", 49.99),
            "Rack of Welsh Lamb": MenuItem("Rack of Welsh Lamb", 24.99),
            "Pan Fried Cod Loin": MenuItem("Pan Fried Cod Loin", 24.99),
            "Charred Cauliflower Steak": MenuItem("Charred Cauliflower Steak", 29.99),
            "Poached Alice Pears": MenuItem("Poached Alice Pears", 8.99),
            "Apricot & Brandy Macaroon": MenuItem("Apricot & Brandy Macaroon", 7.99),
            "Floating Island": MenuItem("Floating Island", 7.99),
            "Dark Chocolate & Strawberry Cheesecake": MenuItem("Dark Chocolate & Strawberry Cheesecake", 8.99),
            "Macadamia Blondie & Chocolate Brownie": MenuItem("Macadamia Blondie & Chocolate Brownie", 8.99),
            "Coffee and biscuits": MenuItem("Coffee and biscuits", 5.99),
        }

    def book_table(self, table_id, session):
        """Book a table for the specified session"""
        if not 1 <= table_id <= 5:
            raise ValueError("Invalid table number. Must be between 1 and 5.")
        return self.tables[table_id - 1].book(session)

    def place_order(self, table_id, session, item_name, quantity=1, diners=1):
        """Place an order for the specified item(s) on a table for the specified session"""
        if session not in ['early', 'late']:
            raise ValueError("Invalid session time. Use 'early' or 'late'.")
        item = self.menu.get(item_name)
        if not item:
            raise ValueError("Menu item not found")
        self.tables[table_id - 1].add_order(session, item, quantity, diners)

    def display_table_status(self):
        """Display the booking status of all tables"""
        for table in self.tables:
            print(f"Table {table.table_id} - Early: {'Booked' if table.booked_sessions['early'] else 'Free'}, "
                  f"Late: {'Booked' if table.booked_sessions['late'] else 'Free'}")

    def generate_report(self):
        """Generate a report containing total income, highest spending table, total tips, and item popularity"""
        total_income = 0
        highest_spending_table = None
        highest_spending = 0
        total_tips = 0
        item_popularity = {}

        for table in self.tables:
            for session in ["early", "late"]:
                if table.booked_sessions[session]:
                    try:
                        bill = table.calculate_bill(session)
                        total_income += bill
                        if bill > highest_spending:
                            highest_spending = bill
                            highest_spending_table = table
                        total_tips += table.tips[session]  # Accumulate tips

                        for item in table.orders[session].items:
                            if item.name in item_popularity:
                                item_popularity[item.name] += 1
                            else:
                                item_popularity[item.name] = 1

                    except Exception as e:
                        print(f"Error processing table {table.table_id}, session {session}: {e}")

        print(f"Total Income: £{total_income:.2f}")
        if highest_spending_table:
            print(f"Highest Spending Table: Table {highest_spending_table.table_id} with £{highest_spending:.2f}")
        print(f"Total Tips: £{total_tips:.2f}")
        print("Item Popularity:")
        for item, count in sorted(item_popularity.items(), key=lambda x: x[1], reverse=True):
            print(f"{item}: {count} orders")

class RestaurantGUI:
    def __init__(self, master, restaurant):
        self.master = master
        self.restaurant = restaurant
        self.master.title("Restaurant Management System")
        self.master.configure(bg='#2E4053')

        self.title_label = tk.Label(self.master, text="Restaurant Management System", font=('Helvetica', 18, 'bold'), bg='#1ABC9C', fg='white')
        self.title_label.pack(pady=10)

        self.book_table_button = tk.Button(self.master, text="Book Table", command=self.book_table, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        self.book_table_button.pack(pady=5)

        self.place_order_button = tk.Button(self.master, text="Place Order", command=self.place_order, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        self.place_order_button.pack(pady=5)

        self.display_status_button = tk.Button(self.master, text="Display Table Status", command=self.display_status, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        self.display_status_button.pack(pady=5)

        self.calculate_bill_button = tk.Button(self.master, text="Calculate Bill", command=self.calculate_bill, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        self.calculate_bill_button.pack(pady=5)

        self.generate_report_button = tk.Button(self.master, text="Generate Report", command=self.generate_report, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        self.generate_report_button.pack(pady=5)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit, bg='#E74C3C', fg='white', font=('Helvetica', 12, 'bold'))
        self.exit_button.pack(pady=5)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def book_table(self):
        def submit_booking():
            table_id = int(table_id_entry.get())
            session = session_entry.get()
            try:
                self.restaurant.book_table(table_id, session)
                messagebox.showinfo("Success", f"Table {table_id} booked for {session} session.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            booking_window.destroy()

        booking_window = tk.Toplevel(self.master)
        booking_window.title("Book Table")
        booking_window.configure(bg='#2E4053', padx=20, pady=20)

        tk.Label(booking_window, text="Table Number (1-5):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        table_id_entry = tk.Entry(booking_window, font=('Helvetica', 12))
        table_id_entry.pack(pady=5)

        tk.Label(booking_window, text="Session (early/late):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        session_entry = tk.Entry(booking_window, font=('Helvetica', 12))
        session_entry.pack(pady=5)

        submit_button = tk.Button(booking_window, text="Submit", command=submit_booking, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        submit_button.pack(pady=10)

        self.center_window(booking_window)

    def place_order(self):
        def submit_order():
            table_id = int(table_id_entry.get())
            session = session_entry.get()
            item_name = item_name_entry.get()
            quantity = int(quantity_entry.get())
            diners = int(diners_entry.get())
            try:
                self.restaurant.place_order(table_id, session, item_name, quantity, diners)
                messagebox.showinfo("Success", f"Order placed for Table {table_id} for {session} session.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            order_window.destroy()

        order_window = tk.Toplevel(self.master)
        order_window.title("Place Order")
        order_window.configure(bg='#2E4053', padx=20, pady=20)

        tk.Label(order_window, text="Table Number (1-5):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        table_id_entry = tk.Entry(order_window, font=('Helvetica', 12))
        table_id_entry.pack(pady=5)

        tk.Label(order_window, text="Session (early/late):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        session_entry = tk.Entry(order_window, font=('Helvetica', 12))
        session_entry.pack(pady=5)

        tk.Label(order_window, text="Item Name:", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        item_name_entry = tk.Entry(order_window, font=('Helvetica', 12))
        item_name_entry.pack(pady=5)

        tk.Label(order_window, text="Quantity:", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        quantity_entry = tk.Entry(order_window, font=('Helvetica', 12))
        quantity_entry.pack(pady=5)

        tk.Label(order_window, text="Number of Diners:", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        diners_entry = tk.Entry(order_window, font=('Helvetica', 12))
        diners_entry.pack(pady=5)

        submit_button = tk.Button(order_window, text="Submit", command=submit_order, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        submit_button.pack(pady=10)

        self.center_window(order_window)

    def display_status(self):
        status_window = tk.Toplevel(self.master)
        status_window.title("Table Status")
        status_window.configure(bg='#2E4053', padx=20, pady=20)

        status_text = tk.Text(status_window, bg='#2E4053', fg='white', font=('Helvetica', 12), wrap='word', padx=10, pady=10)
        status_text.pack(pady=10, fill='both', expand=True)

        for table in self.restaurant.tables:
            status_text.insert(tk.END, f"Table {table.table_id} - Early: {'Booked' if table.booked_sessions['early'] else 'Free'}, "
                                        f"Late: {'Booked' if table.booked_sessions['late'] else 'Free'}\n")

        self.center_window(status_window)

    def calculate_bill(self):
        def submit_bill():
            table_id = int(table_id_entry.get())
            session = session_entry.get()
            payment_method = payment_method_entry.get()
            tip = float(tip_entry.get())
            try:
                total_cost = self.restaurant.tables[table_id - 1].calculate_bill(session, payment_method, tip)
                messagebox.showinfo("Total Bill", f"Total bill for Table {table_id} for {session} session: £{total_cost:.2f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            bill_window.destroy()

        bill_window = tk.Toplevel(self.master)
        bill_window.title("Calculate Bill")
        bill_window.configure(bg='#2E4053', padx=20, pady=20)

        tk.Label(bill_window, text="Table Number (1-5):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        table_id_entry = tk.Entry(bill_window, font=('Helvetica', 12))
        table_id_entry.pack(pady=5)

        tk.Label(bill_window, text="Session (early/late):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        session_entry = tk.Entry(bill_window, font=('Helvetica', 12))
        session_entry.pack(pady=5)

        tk.Label(bill_window, text="Payment Method (cash/credit card):", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        payment_method_entry = tk.Entry(bill_window, font=('Helvetica', 12))
        payment_method_entry.pack(pady=5)

        tk.Label(bill_window, text="Tip Amount:", bg='#2E4053', fg='white', font=('Helvetica', 12)).pack(pady=5)
        tip_entry = tk.Entry(bill_window, font=('Helvetica', 12))
        tip_entry.pack(pady=5)

        submit_button = tk.Button(bill_window, text="Submit", command=submit_bill, bg='#3498DB', fg='white', font=('Helvetica', 12, 'bold'))
        submit_button.pack(pady=10)

        self.center_window(bill_window)

    def generate_report(self):
        report_window = tk.Toplevel(self.master)
        report_window.title("Generate Report")
        report_window.configure(bg='#2E4053', padx=20, pady=20)

        report_text = tk.Text(report_window, bg='#2E4053', fg='white', font=('Helvetica', 12), wrap='word', padx=10, pady=10)
        report_text.pack(pady=10, fill='both', expand=True)

        total_income = 0
        highest_spending_table = None
        highest_spending = 0
        total_tips = 0
        item_popularity = {}

        for table in self.restaurant.tables:
            for session in ["early", "late"]:
                if table.booked_sessions[session]:
                    try:
                        bill = table.calculate_bill(session)
                        total_income += bill
                        if bill > highest_spending:
                            highest_spending = bill
                            highest_spending_table = table
                        total_tips += table.tips[session]

                        for item in table.orders[session].items:
                            if item.name in item_popularity:
                                item_popularity[item.name] += 1
                            else:
                                item_popularity[item.name] = 1

                    except Exception as e:
                        report_text.insert(tk.END, f"Error processing table {table.table_id}, session {session}: {e}\n")

        report_text.insert(tk.END, f"Total Income: £{total_income:.2f}\n")
        if highest_spending_table:
            report_text.insert(tk.END, f"Highest Spending Table: Table {highest_spending_table.table_id} with £{highest_spending:.2f}\n")
        report_text.insert(tk.END, f"Total Tips: £{total_tips:.2f}\n")
        report_text.insert(tk.END, "Item Popularity:\n")
        for item, count in sorted(item_popularity.items(), key=lambda x: x[1], reverse=True):
            report_text.insert(tk.END, f"{item}: {count} orders\n")

        self.center_window(report_window)

if __name__ == "__main__":
    restaurant = Restaurant()

    root = tk.Tk()
    gui = RestaurantGUI(root, restaurant)
    root.mainloop()
