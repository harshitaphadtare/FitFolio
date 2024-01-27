import tkinter as tk #done
from tkinter import ttk#done
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mysql.connector import connect
from datetime import datetime, timedelta #done

# Function to retrieve walking records from the database
def fetch_records(time_range):
    # Replace these placeholders with your actual database credentials
    db_config = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'database': 'your_database'
    }

    # Replace 'your_table_name' with your actual table name
    table_name = 'your_table_name'

    # Replace 'your_date_column' with your actual date column name
    date_column = 'your_date_column'

    # Connect to the database
    connection = connect(**db_config)
    cursor = connection.cursor()

    # Calculate start date based on the time range
    if time_range == '3 days':
        start_date = datetime.now() - timedelta(days=3)
    elif time_range == 'week':
        start_date = datetime.now() - timedelta(weeks=1)
    elif time_range == 'month':
        start_date = datetime.now() - timedelta(weeks=4)
    elif time_range == 'year':
        start_date = datetime.now() - timedelta(weeks=52)
    else:
        # Default to 3 days if the time range is not recognized
        start_date = datetime.now() - timedelta(days=3)

    # Fetch records from the database within the specified time range
    query = f"SELECT {date_column}, distance FROM {table_name} WHERE {date_column} >= %s"
    cursor.execute(query, (start_date,))

    # Fetch the results
    results = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    return results

# Function to create and display the line graph
def show_line_graph(time_range):
    # Fetch walking records
    records = fetch_records(time_range)

    # Extract dates and distances from the records
    dates, distances = zip(*records)

    # Create a line graph using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(dates, distances, marker='o', linestyle='-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance (in miles)')
    ax.set_title(f'Walking Records - {time_range}')

    # Display the graph in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=1, column=0, columnspan=2, pady=10)



#GUI
# Create the main Tkinter window
window = tk.Tk()
window.title('Walking Records App')

# Create a dropdown menu for selecting time range
time_range_label = ttk.Label(window, text='Select Time Range:')
time_range_label.grid(row=0, column=0, pady=10)

time_range_var = tk.StringVar()
time_range_dropdown = ttk.Combobox(window, textvariable=time_range_var, values=['3 days', 'week', 'month', 'year'])
time_range_dropdown.grid(row=0, column=1, pady=10)
time_range_dropdown.set('3 days')  # Set default value

# Button to display the line graph
graph_button = ttk.Button(window, text='Show Graph', command=lambda: show_line_graph(time_range_var.get()))
graph_button.grid(row=0, column=2, pady=10)

# Run the Tkinter event loop
window.mainloop()
