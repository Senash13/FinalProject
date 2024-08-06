# Restaurant Management System
#### Video Demo: [Project Video Demo](https://www.example.com)
#### Description:

The Restaurant Management System is an application designed to help manage the operations of a restaurant efficiently. It is implemented in Python using the `tkinter` library to provide a graphical user interface (GUI). This system allows restaurant staff to book tables, place orders, display table statuses, calculate bills, and generate comprehensive reports. The application aims to streamline the management process, making it easier for staff to handle reservations and orders while keeping track of income and tips.

## Features

### Book Table
Staff can book tables for either the early or late session. The application ensures that each table can only be booked once per session and limits the number of diners to a maximum of eight per table.

### Place Order
Orders can be placed for a specific table and session. The application supports adding multiple items to an order, specifying the quantity of each item, and the number of diners. Priority items like "Fresh Caught Lobster" and "Steak Diane" are handled specially within the system.

### Display Table Status
The current booking status of all tables can be displayed, showing which tables are booked or free for both the early and late sessions. This feature helps staff quickly determine table availability.

### Calculate Bill
The total bill for a table can be calculated, including the option to add a tip and choose the payment method (cash or credit card). The system automatically applies a 10% surcharge for credit card payments and includes the tip in the final bill.

### Generate Report
A comprehensive report can be generated, summarizing total income, highest spending table, total tips, and item popularity. This feature provides valuable insights into the restaurant's performance and helps identify popular menu items.

## Project Structure

### Files and Their Functionality
- `restaurant.py`:  It initializes the restaurant management system and launches the GUI and contains the core classes (`MenuItem`, `Order`, `Table`, and `Restaurant`) that handle the logic of booking tables, placing orders, calculating bills, and generating reports.
Further, implements the `RestaurantGUI` class, which provides the graphical interface for interacting with the system. It includes methods to handle button clicks and display various windows for booking tables, placing orders, etc.

### Classes and Methods

#### `MenuItem`
- `__init__(self, name, price)`: Initializes a menu item with a name and price.
- `__str__(self)`: Returns a string representation of the menu item.

#### `Order`
- `__init__(self)`: Initializes an order with an empty list of items.
- `add_item(self, item, quantity=1)`: Adds a specified quantity of a menu item to the order.
- `total_cost(self)`: Returns the total cost of the order.
- `prioritized_items(self)`: Returns a list of items with priority items first.
- `__str__(self)`: Returns a string representation of the order.

#### `Table`
- `__init__(self, table_id)`: Initializes a table with an ID, booking sessions, orders, diners, and tips.
- `book(self, session)`: Books the table for a specified session.
- `add_order(self, session, item, quantity=1, diners=1)`: Adds an order to the table for a specified session.
- `calculate_bill(self, session, payment_method='cash', tip=0)`: Calculates the total bill for a specified session.
- `__str__(self)`: Returns a string representation of the table.

#### `Restaurant`
- `__init__(self)`: Initializes the restaurant with tables and a menu.
- `load_menu(self)`: Loads the menu dynamically.
- `book_table(self, table_id, session)`: Books a table for a specified session.
- `place_order(self, table_id, session, item_name, quantity=1, diners=1)`: Places an order for a table for a specified session.
- `display_table_status(self)`: Displays the booking status of all tables.
- `generate_report(self)`: Generates a report containing total income, highest spending table, total tips, and item popularity.

#### `RestaurantGUI`
- `__init__(self, master, restaurant)`: Initializes the GUI with the main window and restaurant instance.
- `center_window(self, window)`: Centers a given window on the screen.
- `book_table(self)`: Opens the booking window to book a table.
- `place_order(self)`: Opens the ordering window to place an order.
- `display_status(self)`: Opens the status window to display table statuses.
- `calculate_bill(self)`: Opens the bill window to calculate the total bill.
- `generate_report(self)`: Opens the report window to generate a report.

## Design Choices

### Dynamic Menu Loading
The menu is loaded dynamically from a dictionary, making it easy to update or modify the menu items without changing the core application logic.

### Table Booking System
The booking system ensures that each table can only be booked once per session, preventing overbooking and maintaining a clear record of reservations.

### Priority Items
Certain menu items are given priority in the order list to highlight their importance. This feature is implemented to manage high-demand items more efficiently.

### GUI Implementation
The `tkinter` library is used to provide a simple yet functional GUI. The interface is designed to be intuitive and easy to navigate, with buttons and entry fields for various functionalities.

### Error Handling
The application includes error handling to manage invalid inputs and operations gracefully. This ensures a smooth user experience and prevents crashes due to incorrect data.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

