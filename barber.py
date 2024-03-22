import re
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


# Declare content_frame as a global variable
content_frame = None  

# Database connection and cursor
try:
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
except sqlite3.Error as e:
    messagebox.showerror("Database Error", f"Error connecting to database: {e}")
    exit()


def create_table():
    try:
        # Create the orders table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                telephone VARCHAR(20),
                service TEXT,
                barber TEXT,
                date TEXT,
                time TEXT
            )
        """)
        # Commit changes to the database
        conn.commit()
    except sqlite3.Error as e:
        # Show an error message if there's an issue with creating the table
        messagebox.showerror("Database Error", f"Error creating orders table: {e}")


def insert_order(name, telephone, service, barber, date, time):
    try:
        # Insert a new order into the database
        cursor.execute("""
            INSERT INTO orders (name, telephone, service, barber, date, time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, telephone, service, barber, date, time))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error inserting order: {e}")


def delete_order(order_id):
    try:
        # Delete an order from the database
        cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error deleting order: {e}")


def update_order(order_id, name, telephone, service, barber, date, time):
    try:
        # Update an order in the database
        cursor.execute("""
            UPDATE orders 
            SET name=?, telephone=?, service=?, barber=?, date=?, time=?
            WHERE id=?
        """, (name, telephone, service, barber, date, time, order_id))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error updating order: {e}")


def fetch_orders():
    try:
        # Fetch all orders from the database
        cursor.execute("SELECT * FROM orders")
        # Return the fetched orders
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching orders: {e}")
        # Return an empty list
        return []


create_table()


def navigate_to(section):
    # Access the global content_frame variable
    global content_frame  

    # Clear the current content frame
    content_frame.pack_forget()

    # Create a new content frame
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Display different content based on the selected section
    if section == "Home":
        #home section title & description
        welcome_label = tk.Label(content_frame, text="Welcome to Barbershop", font=("Arial", 20, "bold"), bg="white")
        info_label = tk.Label(content_frame, text="Please Fill Out the Form Below to Book Your Appointment.", font=("Arial", 12), bg="white")
        

        #home section form inputs & labels
        service_label = tk.Label(content_frame, text="Service:", font=("Arial", 12), bg="white")
        service_combobox = ttk.Combobox(content_frame, font=("Arial", 12), values=["Regular cut", "Fade cut", "Crew cut", "Beard trim", "Hair color", "Wash, Trim & Style"])
        barber_label = tk.Label(content_frame, text="Stylist:", font=("Arial", 12), bg="white")
        barber_combobox = ttk.Combobox(content_frame, font=("Arial", 12), values=["Ephrem", "Michael", "Addisu", "Mulugeta", "Hirut"])
        date_label = tk.Label(content_frame, text="Date:", font=("Arial", 12), bg="white")
        date_combobox = ttk.Combobox(content_frame, font=("Arial", 12), values=["2024-03-22", "2024-03-23", "2024-03-24", "2024-03-25"])
        time_label = tk.Label(content_frame, text="Time:", font=("Arial", 12), bg="white")
        time_combobox = ttk.Combobox(content_frame, font=("Arial", 12), values=["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM"])
        name_label = tk.Label(content_frame, text="Full Name:", font=("Arial", 12), bg="white")
        name_entry = ttk.Entry(content_frame, font=("Arial", 12), width=22)
        telephone_label = tk.Label(content_frame, text="Telephone:", font=("Arial", 12), bg="white")
        telephone_entry = ttk.Entry(content_frame, font=("Arial", 12), width=22)


        # grid home section & form contents
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        service_label.grid(row=2, column=0, sticky=tk.E, padx=20)
        service_combobox.grid(row=2, column=1, padx=20, pady=5, sticky=tk.W)
        barber_label.grid(row=3, column=0, sticky=tk.E, padx=20)
        barber_combobox.grid(row=3, column=1, padx=20, pady=5, sticky=tk.W)
        date_label.grid(row=4, column=0, sticky=tk.E, padx=20)
        date_combobox.grid(row=4, column=1, padx=20, pady=5, sticky=tk.W)
        time_label.grid(row=5, column=0, sticky=tk.E, padx=20)
        time_combobox.grid(row=5, column=1, padx=20, pady=5, sticky=tk.W)
        name_label.grid(row=6, column=0, sticky=tk.E, padx=20)
        name_entry.grid(row=6, column=1, padx=20, pady=5, sticky=tk.W)
        telephone_label.grid(row=7, column=0, sticky=tk.E, padx=20)
        telephone_entry.grid(row=7, column=1, padx=20, pady=5, sticky=tk.W)


        # Validate phone number
        def validate_phone_number(phone_number):
            # regular expression pattern for Ethiopian phone numbers
            pattern = r'^(?:\+2519|\d{2})\d{8}$'

            # Check if the phone number matches the pattern
            if re.match(pattern, phone_number):
                return True
            else:
                return False
            

        # Handle submissions 
        def schedule():
            # Create the orders table if it doesn't exist
            create_table()


            # Retrieve input values
            name = name_entry.get()
            telephone = telephone_entry.get()
            service = service_combobox.get()
            barber = barber_combobox.get()
            date = date_combobox.get()
            time = time_combobox.get()


            # Input validation
            if not (name and telephone and service and barber and date and time):
                messagebox.showerror("Input Error", "All fields are required.")

            elif not validate_phone_number(telephone):
                messagebox.showerror("Input Error", "Please enter a valid phone number.")

            else:
                # Insert order into the database
                insert_order(name, telephone, service, barber, date, time)
                messagebox.showinfo("Thank You!", "Thanks for choosing us! Can't wait to style your hair!")
                

                # Clear input fields
                name_entry.delete(0, tk.END)
                telephone_entry.delete(0, tk.END)
                service_combobox.set('')
                barber_combobox.set('')
                date_combobox.set('')
                time_combobox.set('')


        # Submit button
        submit_button = tk.Button(content_frame, text="Schedule", font=("Arial", 12, "bold"), bg="#333", fg="white", width=20, command=schedule)
        submit_button.grid(row=8, column=1, padx=17, pady=5, sticky=tk.W)
        
        
        # Center contents on column 1 & 2
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
    
    elif section == "About":
        #about section content
        about_title_label = tk.Label(content_frame, text="About Us", font=("Arial", 20, "bold"), bg="white")
        about_text = "Barbershop is a team of highly qualified barbers dedicated to offering the best value.\nWe do this by providing high quality salon services for men and boys, in a warm, friendly atmosphere."
        about_label = tk.Label(content_frame, text=about_text, font=("Arial", 12), bg="white", justify="center")


        #pack contents
        about_title_label.pack(pady=(20, 10))
        about_label.pack(pady=(0, 10))
    
    elif section == "Services":
        # Services section content
        services_title_label = tk.Label(content_frame, text="Services", font=("Arial", 20, "bold"), bg="white")
        services_title_label.pack(pady=(20, 10))


        # Service names and prices display
        service_data = [
            ("100.00 Br", "HAIRCUT"),
            ("150.00 Br", "HAIRCUT + BEARD"),
            ("70.00 Br", "BEARD TRIM"),
            ("80.00 Br", "HAIR COLOR"),
            ("180.00 Br", "WASH, TRIM & STYLE")
        ]


        # Create a frame for services
        services_frame = tk.Frame(content_frame, bg="white")
        services_frame.pack(pady=(0, 10))


        for service_price, service_name in service_data:
            # Create a frame for each service group
            group_frame = tk.Frame(services_frame, bg="white")


            #Create label for service price & name
            price_label = tk.Label(group_frame, text=service_price, font=("Arial", 12, "bold"), bg="white")
            service_label = tk.Label(group_frame, text=service_name, font=("Arial", 12), bg="white")

            #pack
            group_frame.pack(side=tk.LEFT, padx=10)
            service_label.pack()
            price_label.pack()
    
    elif section == "Orders":
        # Orders section title label
        orders_title_label = tk.Label(content_frame, text="Orders", font=("Arial", 20, "bold"), bg="white")
        orders_title_label.pack(pady=(20, 10))


        # Fetched data for the table
        fetched_data = fetch_orders()


        # Table creation
        table = ttk.Treeview(content_frame, columns=["Id", "Name", "Telephone", "Service", "Barber", "Date", "Time"], show="headings")
        table.pack(pady=(0, 10))


        # Define column headings for the table
        table.heading("Id", text="Id")
        table.heading("Name", text="Name")
        table.heading("Telephone", text="Telephone")
        table.heading("Service", text="Service")
        table.heading("Barber", text="Stylist")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")


        # Insert fetched data into the table
        for data in fetched_data:
            table.insert("", "end", values=(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6]
            ))

        
        # Handling update
        def update_selected():
            # Get the selected item
            selected_item = table.selection()[0]


            # Get the values of the selected item
            values = table.item(selected_item, "values")


            # Open a new window for updating the selected item
            update_window = tk.Toplevel(root)
            update_window.title("Update Order")


            # Create labels and entries for updating the order
            name_label = tk.Label(update_window, text="Name:", font=("Arial", 12))
            name_entry = tk.Entry(update_window, font=("Arial", 12))
            telephone_label = tk.Label(update_window, text="Phone:", font=("Arial", 12))
            telephone_entry = tk.Entry(update_window, font=("Arial", 12))
            service_label = tk.Label(update_window, text="Service:", font=("Arial", 12))
            service_entry = tk.Entry(update_window, font=("Arial", 12))
            barber_label = tk.Label(update_window, text="Stylist:", font=("Arial", 12))
            barber_entry = tk.Entry(update_window, font=("Arial", 12))
            date_label = tk.Label(update_window, text="Date:", font=("Arial", 12))
            date_entry = tk.Entry(update_window, font=("Arial", 12))
            time_label = tk.Label(update_window, text="Time:", font=("Arial", 12))
            time_entry = tk.Entry(update_window, font=("Arial", 12))


            #grid labels & entries
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
            name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
            telephone_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
            telephone_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
            service_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
            service_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
            barber_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
            barber_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
            date_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
            date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
            time_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
            time_entry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)


            # Insert the current values of the selected order into the entry fields
            name_entry.insert(0, values[1])
            telephone_entry.insert(0, values[2])
            service_entry.insert(0, values[3])
            barber_entry.insert(0, values[4])
            date_entry.insert(0, values[5])
            time_entry.insert(0, values[6])


            #On click of update button
            def update():
                # Update the order with the new values
                update_order(values[0], name_entry.get(), telephone_entry.get(), service_entry.get(), barber_entry.get(), date_entry.get(), time_entry.get())
                
                # Close the update window
                update_window.destroy()

                # Navigate back to the orders section
                navigate_to("Orders")


            # Update button
            update_button = tk.Button(update_window, text="Update", font=("Arial", 12, "bold"), bg="#333", fg="white", command=update)
            update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        

        # Handling delete
        def delete_selected():
            # Get the selected item
            selected_item = table.selection()[0]

            # Get the values of the selected item
            values = table.item(selected_item, "values")

            # Confirm deletion
            confirmation = messagebox.askyesno("Delete Order", f"Are you sure you want to delete the order for {values[1]}?")

            
            if confirmation:
                # Delete the order with the specified ID
                delete_order(values[0])

                # Navigate back to the orders section
                navigate_to("Orders")  


        # Update & Delete buttons
        update_button = tk.Button(content_frame, text="Update", font=("Arial", 12, "bold"), bg="#333", fg="white", command=update_selected, state=tk.DISABLED)
        delete_button = tk.Button(content_frame, text="Delete", font=("Arial", 12, "bold"), bg="#333", fg="white", command=delete_selected, state=tk.DISABLED)


        # Pack buttons
        update_button.pack(side=tk.LEFT, padx=10)
        delete_button.pack(side=tk.LEFT, padx=10)


        # Function to check and enable/disable buttons based on data availability
        def update_buttons_state():
            if len(fetched_data) > 0:
                update_button.config(state=tk.NORMAL)
                delete_button.config(state=tk.NORMAL)
            else:
                update_button.config(state=tk.DISABLED)
                delete_button.config(state=tk.DISABLED)


        update_buttons_state()


root = tk.Tk()
root.title("Barber Shop - Style at Your Fingertips.")
root.iconbitmap("./assets/icon.ico")


#frames
navbar_frame = tk.Frame(root, bg="#333", width=150)
content_frame = tk.Frame(root, bg="white")

#nav sections
brand_label = tk.Label(navbar_frame, text="Barber", font=("Arial", 20, "bold"), fg="white", bg="#333")
home_button = tk.Button(navbar_frame, text="Home", bg="#333", fg="white", padx=10, pady=5, font=font.Font(weight="normal"), command=lambda: navigate_to("Home"))
about_button = tk.Button(navbar_frame, text="About", bg="#333", fg="white", padx=10, pady=5, font=font.Font(weight="normal"), command=lambda: navigate_to("About"))
services_button = tk.Button(navbar_frame, text="Services", bg="#333", fg="white", padx=10, pady=5, font=font.Font(weight="normal"), command=lambda: navigate_to("Services"))
orders_button = tk.Button(navbar_frame, text="Orders", bg="#333", fg="white", padx=10, pady=5, font=font.Font(weight="normal"), command=lambda: navigate_to("Orders"))
faq_button = tk.Button(navbar_frame, text="FAQs", bg="#333", fg="white", padx=10, pady=5, font=font.Font(weight="normal"), command=lambda: navigate_to("Orders"))


#pack nav sections
brand_label.pack(fill=tk.X, pady=10)
home_button.pack(fill=tk.X)
about_button.pack(fill=tk.X)
services_button.pack(fill=tk.X)
orders_button.pack(fill=tk.X)   
faq_button.pack(fill=tk.X)   


#pack frames
navbar_frame.pack(side=tk.LEFT, fill=tk.Y)
content_frame.pack(fill=tk.BOTH, expand=True)


#display the home section by default
navigate_to("Home")


root.mainloop()
