import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Order Management")

        # Database connection parameters
        self.db_params = {
            'dbname': 'db-magang',
            'user': 'magang',
            'password': 'magangm1d1',
            'host': '34.101.181.164',  # or your database host
            'port': '5432'  # default PostgreSQL port
        }

        # Table Setup
        self.tree = ttk.Treeview(root, columns=('Order ID', 'Customer', 'Item', 'Notes'), show='headings', height=8)
        self.tree.heading('Order ID', text='Order ID')
        self.tree.heading('Customer', text='Customer')
        self.tree.heading('Item', text='Item')
        self.tree.heading('Notes', text='Notes')
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Fetch Orders Button
        self.fetch_button = ttk.Button(root, text="Fetch Orders", command=self.fetch_orders)
        self.fetch_button.grid(row=1, column=0, padx=10, pady=10)

        # Print Button
        self.print_button = ttk.Button(root, text="Print Order", command=self.print_order)
        self.print_button.grid(row=1, column=1, padx=10, pady=10)

        # Exit Button
        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=1, column=2, padx=10, pady=10)

    def fetch_orders(self):
        # Clear any existing orders in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Connect to the database
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()

            # Fetch orders from the database
            cursor.execute("SELECT order_id, customer_name, item, notes FROM order_label")
            orders = cursor.fetchall()

            # Insert the fetched orders into the tree
            for order in orders:
                self.tree.insert('', 'end', values=order)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching orders:\n{str(e)}")

    def print_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an order to print.")
            return

        # Get selected order details
        order_details = self.tree.item(selected_item, 'values')
        order_id, customer, item, notes = order_details

        # Print the label (Here we're just showing it in a messagebox)
        label_text = f"Customer Name : {customer}\nItem : {item}\nNotes : {notes}\nOrder ID : {order_id}"
        messagebox.showinfo("Order Label", label_text)

        # Remove the order from the list
        self.tree.delete(selected_item)

        try:
            # Connect to the database
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()

            # Remove the order from the database
            cursor.execute("DELETE FROM order_label WHERE order_id = %s AND customer_name = %s AND item = %s",
                           (order_id, customer, item))
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while deleting the order:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeOrderApp(root)
    root.mainloop()
