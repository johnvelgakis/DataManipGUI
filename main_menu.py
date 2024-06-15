import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from db_connection import connect_to_db, insert_booking_data
from sqlalchemy import create_engine

'''
Hotels Booking Data Analysis and Presentation GUI

This script provides a graphical user interface (GUI) for analyzing and presenting hotel booking data. The GUI comprises 
multiple pages, each displaying different aspects of the data analysis, derived from MySQL database queries. It allows 
users to interact with the data visually and retrieve information seamlessly.

Overview:
---------
The GUI structure is based on the `GUI_Window` class, from which other classes inherit to create various pages. These pages 
are designed to display statistical analyses and visualizations of hotel booking data. All data manipulations are performed 
using Pandas DataFrame objects.

Data Handling:
--------------
For each page, data is fetched from the MySQL database and loaded into a Pandas DataFrame using the following code snippet:
    
    connection = connect_to_db()
    df = pd.read_sql("SELECT * FROM bookings", connection)

Post data manipulation, results are displayed using graphical widgets and saved locally as .png images and updated tables 
in the MySQL database. Each page ensures that a single file or table per analysis is saved, replacing any existing files.

Initial Data Upload:
--------------------
The initial data upload involves reading data from a CSV file and inserting it into the MySQL database. Run insert_data_to_DB.py.



After each manipulation, the resultant table is uploaded back to the database using the following function:
    
    upload_to_db(max_min_data, 'booking_distribution')

The CSV versions of these tables can be found in the 'tables' directory.

Key Functionalities:
--------------------
- Interactive GUI for data analysis
- Data retrieval from MySQL database
- Data manipulation and analysis using Pandas
- Visualization of results using Matplotlib
- Saving analysis results as .png images and updating MySQL tables

'''

script_dir = os.path.dirname(__file__)

def upload_to_db(df, table_name):
    connection = connect_to_db()
    engine = create_engine('mysql+mysqlconnector://root:ArxesGlwsswn1!@localhost/hotel_booking')
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    connection.close()


def confirm_quit(parent):
    response = messagebox.askyesno("Τερματισμός;", "Είστε σίγουροι ότι θέλετε να τερματίσετε;")
    if response:
        parent.destroy()


class GUI_Window:
    def __init__(self, root):
        '''
        Class Constructor for the GUI_Window class
        '''
        self.root = root
        self.root.title("Hotel Booking Main Menu")
        self.root.geometry('655x300')
        self.create_main_menu()

    def create_main_menu(self):
        image_path = os.path.join(script_dir, "media/src/bg1.jpg")  
        image = Image.open(image_path)
        image = image.resize((655, 300), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.root, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)
        main_frame = tk.Frame(self.root, bg='#686D76')
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=0, padx=10, pady=10)

        buttons = [
            ('Βασικά Στατιστικά Στοιχεία', self.open_basic_statistics),
            ('Κατανομές Σταστικών', self.open_booking_dist),
            ('Τάσεις Σταστικών', self.open_booking_trends),
            ('Εποχικότητα Στατιστικών', self.open_seasonality)
        ]
        for text, command in buttons:
            button = tk.Button(button_frame, text=text, bg='#EEEEEE', fg='#373A40', command=command)
            button.pack(pady=10)

        dropdown_frame = tk.Frame(main_frame)
        dropdown_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(dropdown_frame, text="Κατανομές Δεδομένων").grid(row=0, column=0, padx=5, pady=5)
        self.booking_dist_option = ttk.Combobox(dropdown_frame, values=['ανά μήνα', 'ανά εποχή', 'ανά τύπο δωματίου', 'ανά πελάτη'], state='readonly', justify='center')
        self.booking_dist_option.grid(row=0, column=1, padx=5, pady=5)
        self.booking_dist_option.current(0)

        tk.Label(dropdown_frame, text="Τάσεις Δεδομένων").grid(row=1, column=0, padx=5, pady=5)
        self.booking_trends_option = ttk.Combobox(dropdown_frame, values=['μηνιαίες τάσεις', 'ετήσιες τάσεις', 'εποχιακές τάσεις', 'συγκριτικές τάσεις'], state='readonly', justify='center')
        self.booking_trends_option.grid(row=1, column=1, padx=5, pady=5)
        self.booking_trends_option.current(0)

        self.var_total = tk.BooleanVar(value=True)
        self.var_custom = tk.BooleanVar(value=False)

        total_checkbox = tk.Checkbutton(dropdown_frame, text="Συνολικά Στοιχεία", variable=self.var_total, command=self.toggle_date_fields)
        total_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        custom_checkbox = tk.Checkbutton(dropdown_frame, text="Στοιχεία Custom Περιόδου", variable=self.var_custom, command=self.toggle_date_fields)
        custom_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.date_min_label = tk.Label(dropdown_frame, text="Ημερομηνία Από")
        self.date_min = tk.Entry(dropdown_frame)
        self.date_min.insert(0, "YYYY-MM-DD")

        self.date_max_label = tk.Label(dropdown_frame, text="Ημερομηνία Έως")
        self.date_max = tk.Entry(dropdown_frame)
        self.date_max.insert(0, "YYYY-MM-DD")

        self.toggle_date_fields()

        bottom_left_label = tk.Label(self.root, text="Προαιρετική Εργαστηριακή Άσκηση Python\nΑρχές Γλωσσών Προγραμματισμού & Μεταφραστών\n2023-2024", font=("Helvetica", 12, "italic"), bg='#686D76', fg='white')
        bottom_left_label.place(relx=0.01, rely=0.95, anchor=tk.SW)

        bottom_right_label = tk.Label(self.root, text="Ιωάννης Βελγάκης\n1047071", font=("Helvetica", 12), bg='#686D76', fg='white')
        bottom_right_label.place(relx=0.99, rely=0.95, anchor=tk.SE)

        quit_button = tk.Button(self.root, text='Quit', command=lambda: confirm_quit(self.root))
        quit_button.place(relx=0.95, rely=0.05, anchor=tk.NE)

    def toggle_date_fields(self):
        if self.var_custom.get():
            self.date_min_label.grid(row=3, column=0, padx=5, pady=5)
            self.date_min.grid(row=3, column=1, padx=5, pady=5)
            self.date_max_label.grid(row=4, column=0, padx=5, pady=5)
            self.date_max.grid(row=4, column=1, padx=5, pady=5)
        else:
            self.date_min_label.grid_remove()
            self.date_min.grid_remove()
            self.date_max_label.grid_remove()
            self.date_max.grid_remove()

    def open_basic_statistics(self):
        if self.var_custom.get():
            date_min = self.date_min.get()
            date_max = self.date_max.get()
            BasicStatistics(self.root, date_min, date_max)
        else:
            BasicStatistics(self.root, None, None)

    def open_booking_dist(self):
        option = self.booking_dist_option.get()
        if self.var_custom.get():
            date_min = self.date_min.get()
            date_max = self.date_max.get()
            BookingDist(self.root, option, date_min, date_max)
        else:
            BookingDist(self.root, option, None, None)

    def open_booking_trends(self):
        option = self.booking_trends_option.get()
        if self.var_custom.get():
            date_min = self.date_min.get()
            date_max = self.date_max.get()
            BookingTrends(self.root, option, date_min, date_max)
        else:
            BookingTrends(self.root, option, None, None)

    def open_seasonality(self):
        if self.var_custom.get():
            date_min = self.date_min.get()
            date_max = self.date_max.get()
            Seasonality(self.root, date_min, date_max)
        else:
            Seasonality(self.root, None, None)


class BasicStatistics(tk.Toplevel):
    def __init__(self, master, date_min, date_max):
        super().__init__(master)
        self.geometry('1350x800')
        self.date_min = pd.to_datetime(date_min) if date_min else None
        self.date_max = pd.to_datetime(date_max) if date_max else None
        self.style = ttk.Style()
        self.style.configure('TButton', background='#EEEEEE', foreground='#373A40')
        self.create_widgets()

    def create_widgets(self):
        image_path = os.path.join(script_dir, "media/src/bg1.jpg")  
        image = Image.open(image_path)
        image = image.resize((1350, 800), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        connection = connect_to_db()
        df = pd.read_sql("SELECT * FROM bookings", connection)
        connection.close()

        df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-01')

        if self.date_min and self.date_max:
            df = df[(df['arrival_date'] >= self.date_min) & (df['arrival_date'] <= self.date_max)]
            timeInterval = f' από {self.date_min.strftime("%Y-%m-%d")} εώς {self.date_max.strftime("%Y-%m-%d")}'
        else:
            timeInterval = '. '
        self.title(f'Βασικά Στατιστικά Στοιχεία{timeInterval}')

        df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

        basic_stats = df.groupby('hotel').agg(
            average_nights=('total_nights', 'mean'),
            cancellation_rate=('is_canceled', 'mean'),
            first_arrival=('arrival_date', 'min'),
            last_arrival=('arrival_date', 'max'),
            total_cancellations=('is_canceled', 'sum'),
            total_bookings=('is_canceled', 'count')
        ).reset_index()
        basic_stats['cancellation_percentage'] = basic_stats['cancellation_rate'] * 100
        upload_to_db(basic_stats, 'basic_statistics')

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5))

        # Average Nights Spent per Hotel
        bars1 = ax1.bar(basic_stats['hotel'], basic_stats['average_nights'], color='g', alpha=0.6, label='Average Nights Spent')
        ax1.set_xlabel('Ξενοδοχείο')
        ax1.set_ylabel('Μ.Ο. Διανυκτερεύσεων')
        ax1.set_title('Διανυκτερεύσεις ανά Ξενοδοχείο')

        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{height:.2f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height), 
                        xytext=(0, 3), 
                        textcoords="offset points", 
                        ha='center', va='bottom')

        # Cancellation Percentage per Hotel
        bars2 = ax2.bar(basic_stats['hotel'], basic_stats['cancellation_percentage'], color='r', alpha=0.6, label='Cancellation Percentage')
        ax2.set_xlabel('Ξενοδοχείο')
        ax2.set_ylabel('Ποσοστό Ακυρώσεων')
        ax2.set_title('Ακυρώσεις ανά Ξενοδοχείο')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height:.2f}%', 
                        xy=(bar.get_x() + bar.get_width() / 2, height), 
                        xytext=(0, 3), 
                        textcoords="offset points", 
                        ha='center', va='bottom')

        plt.tight_layout()
    

        plot_filename = os.path.join(script_dir, 'media/graphics/basic_statistics.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=6, padx=20, pady=10, sticky='e')
        
        bold_label = tk.Label(self, text="Βασικά Στατιστικά Ξενοδοχείων", font=("Helvetica", 16, "bold"))
        bold_label.grid(row=0, column=1, padx=1, pady=1)

        canvas = tk.Canvas(self, width=980, height=200, bg='black') 
        canvas.grid(row=1, column=0, padx=5, pady=1)

        # Define table dimensions
        cell_width = 140
        cell_height = 40
        cols = 7
        rows = len(basic_stats) + 1  

        # Draw table grid
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                canvas.create_rectangle(x1, y1, x2, y2)

        headers = ["Ξενοδοχείο", "Συνολικές Κρατήσεις", "Συνολικές Ακυρώσεις", "Ακυρώσεις %", "Μ.Ο. Διανυκτερεύσεων", "Πρώτη Κράτηση", "Τελευταία Κράτηση"]
        for j, header in enumerate(headers):
            x = j * cell_width + cell_width / 2
            y = cell_height / 2
            canvas.create_text(x, y, text=header, font=("Helvetica", 12, "bold") )

        for i, row in basic_stats.iterrows():
            canvas.create_text(cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['hotel'], font=("Helvetica", 12, "italic"))
            canvas.create_text(cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=f"{row['total_bookings']}")
            canvas.create_text(2 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=f"{row['total_cancellations']}")
            canvas.create_text(3 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=f"{row['cancellation_percentage']:.2f}%")
            canvas.create_text(4 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=f"{row['average_nights']:.2f}")
            canvas.create_text(5 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['first_arrival'].strftime('%Y-%m-%d'))
            canvas.create_text(6 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['last_arrival'].strftime('%Y-%m-%d'))

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=4, padx=10, pady=10, sticky='e')


class BookingDist(tk.Toplevel):
    def __init__(self, master, option, date_min, date_max):
        super().__init__(master)
        self.title(f"Κατανομές Κρατήσεων από {date_min} εώς {date_max}")
        self.geometry('1200x1050')
        self.option = option
        self.date_min = date_min
        self.date_max = date_max
        self.style = ttk.Style()
        self.style.configure('TButton', background='#EEEEEE', foreground='#373A40')
        self.create_widgets()
    

    def create_widgets(self):
        image_path = os.path.join(script_dir, "media/src/bg1.jpg")  
        image = Image.open(image_path)
        image = image.resize((1200, 1050), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(image)
        
        self.bg_label = tk.Label(self, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        connection = connect_to_db()
        df = pd.read_sql("SELECT * FROM bookings", connection)
        connection.close()
        
        df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-01')
        
        if isinstance(self.date_min, str):
            self.date_min = pd.to_datetime(self.date_min)
        if isinstance(self.date_max, str):
            self.date_max = pd.to_datetime(self.date_max)

        if self.date_min and self.date_max:
            df = df[(df['arrival_date'] >= self.date_min) & (df['arrival_date'] <= self.date_max)]
            timeInterval = f' από {self.date_min.strftime("%Y-%m-%d")} εώς {self.date_max.strftime("%Y-%m-%d")}'
        else:
            timeInterval = '. '
        self.title(f'Κατανομη Στατιστικών{timeInterval}')

        if self.option == 'ανά μήνα':
            self.plot_by_month(df)
        elif self.option == 'ανά εποχή':
            self.plot_by_season(df)
        elif self.option == 'ανά τύπο δωματίου':
            self.plot_by_room_type(df)
        elif self.option == 'ανά πελάτη':
            self.plot_by_client(df)

        max_min_data = self.get_max_min_data(df)
        upload_to_db(max_min_data, 'booking_distribution')

        bold_label = tk.Label(self, text="Κατανομές Κρατήσεων Ξενοδοχείων", font=("Helvetica", 16, "bold"))
        bold_label.grid(row=0, column=1, padx=1, pady=1)
        # Table
        canvas = tk.Canvas(self, width=810, height=160, bg='black')
        canvas.grid(row=1, column=0, padx=1, pady=1)
        cell_width = 90
        cell_height = 40
        cols = 9
        rows = len(max_min_data) + 1 
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                canvas.create_rectangle(x1, y1, x2, y2)
        canvas.create_line(0, 0, cols * cell_width, 0, width=2)  # Top line of header
        canvas.create_line(0, 0, 0, rows * cell_height, width=2)  # Left line of leftmost column

        headers = ["Ξενοδοχείο", "Μήνας Max", "Μήνας Min", "Εποχή Max", "Εποχή Min", "Δωμάτιο Max", "Δωμάτιο Min", "Πελάτης Max", "Πελάτης Min"]
        for j, header in enumerate(headers):
            x = j * cell_width + cell_width / 2
            y = cell_height / 2
            canvas.create_text(x, y, text=header, font=("Helvetica", 12, "bold"))

        for i, row in max_min_data.iterrows():
            canvas.create_text(cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['hotel'], font=("Helvetica", 12, "italic"))
            canvas.create_text(cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['max_month'])
            canvas.create_text(2 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['min_month'])
            canvas.create_text(3 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['max_season'])
            canvas.create_text(4 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['min_season'])
            canvas.create_text(5 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['max_room_type'])
            canvas.create_text(6 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['min_room_type'])
            canvas.create_text(7 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['max_client_type'])
            canvas.create_text(8 * cell_width + cell_width / 2, (i + 1) * cell_height + cell_height / 2, text=row['min_client_type'])

    def get_max_min_data(self, df):
        season_map = {
            'January': 'Χειμώνας', 'February': 'Χειμώνας', 'March': 'Άνοιξη',
            'April': 'Άνοιξη', 'May': 'Άνοιξη', 'June': 'Καλοκαίρι',
            'July': 'Καλοκαίρι', 'August': 'Καλοκαίρι', 'September': 'Φθινόπωρο',
            'October': 'Φθινόπωρο', 'November': 'Φθινόπωρο', 'December': 'Χειμώνας'
        }
        df['season'] = df['arrival_date_month'].map(season_map)

        conditions = [
            (df['adults'] > 1) & (df['children'] + df['babies'] > 0),
            (df['adults'] > 1) & (df['children'] + df['babies'] == 0),
            (df['adults'] == 1) & (df['children'] + df['babies'] == 0)
        ]
        choices = ['Οικογένεια', 'Ζευγάρι', 'Μεμονωμένοι Ταξιδιώτες']
        df['customer_type'] = np.select(conditions, choices, default='Other')

        max_min_data = []

        for hotel in df['hotel'].unique():
            hotel_data = df[df['hotel'] == hotel]

            max_month = hotel_data['arrival_date_month'].value_counts().idxmax()
            min_month = hotel_data['arrival_date_month'].value_counts().idxmin()

            max_season = hotel_data['season'].value_counts().idxmax()
            min_season = hotel_data['season'].value_counts().idxmin()

            max_room_type = hotel_data['reserved_room_type'].value_counts().idxmax()
            min_room_type = hotel_data['reserved_room_type'].value_counts().idxmin()

            hotel_data_filtered = hotel_data[hotel_data['customer_type'] != 'Other']
            max_client_type = hotel_data_filtered['customer_type'].value_counts().idxmax() if not hotel_data_filtered.empty else 'N/A'
            min_client_type = hotel_data_filtered['customer_type'].value_counts().idxmin() if not hotel_data_filtered.empty else 'N/A'

            max_min_data.append([hotel, max_month, min_month, max_season, min_season, max_room_type, min_room_type, max_client_type, min_client_type])

        return pd.DataFrame(max_min_data, columns=['hotel', 'max_month', 'min_month', 'max_season', 'min_season', 'max_room_type', 'min_room_type', 'max_client_type', 'min_client_type'])

    def plot_by_month(self, df):
        booking_dist = df.groupby(['hotel', 'arrival_date_month']).size().unstack(fill_value=0).reindex(columns=[
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        ], fill_value=0)

        hotels = booking_dist.index
        fig, axes = plt.subplots(len(hotels), 1, figsize=(5, 3 * len(hotels)))

        if len(hotels) == 1:
            axes = [axes]

        for ax, hotel in zip(axes, hotels):
            bars = ax.bar(booking_dist.columns, booking_dist.loc[hotel], color='skyblue')
            ax.set_xlabel('Μήνας')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Μηνιαία Κατανομή Κρατήσεων για το {hotel}')
            ax.tick_params(axis='x', rotation=45)

            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}', 
                            xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(0, 3), 
                            textcoords="offset points", 
                            ha='center', va='top', rotation=90)
        
        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/monthly_distribution.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=2, column=0, columnspan=2, padx=1, pady=1)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=6, padx=1, pady=1, sticky='e')

    def plot_by_season(self, df):
        season_map = {
            'January': 'Χειμώνας', 'February': 'Χειμώνας', 'March': 'Άνοιξη',
            'April': 'Άνοιξη', 'May': 'Άνοιξη', 'June': 'Καλοκαίρι',
            'July': 'Καλοκαίρι', 'August': 'Καλοκαίρι', 'September': 'Φθινόπωρο',
            'October': 'Φθινόπωρο', 'November': 'Φθινόπωρο', 'December': 'Χειμώνας'
        }
        df['season'] = df['arrival_date_month'].map(season_map)
        booking_dist = df.groupby(['hotel', 'season']).size().unstack(fill_value=0)

        hotels = booking_dist.index
        fig, axes = plt.subplots(len(hotels), 1, figsize=(5, 3 * len(hotels)))

        if len(hotels) == 1:
            axes = [axes]

        for ax, hotel in zip(axes, hotels):
            bars = ax.bar(booking_dist.columns, booking_dist.loc[hotel], color='skyblue')
            ax.set_xlabel('Εποχή')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Κατανομή Κρατήσεων ανά εποχή για το {hotel}')
            ax.tick_params(axis='x', rotation=45)

            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}', 
                            xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(0, 3), 
                            textcoords="offset points", 
                            ha='center', va='bottom', rotation=30)

        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/seasonal_distribution.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=2, column=0, columnspan=2, padx=1, pady=1)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=6, padx=1, pady=1, sticky='e')

    def plot_by_room_type(self, df):
        booking_dist = df.groupby(['hotel', 'reserved_room_type']).size().unstack(fill_value=0)

        hotels = booking_dist.index
        fig, axes = plt.subplots(len(hotels), 1, figsize=(5, 3 * len(hotels)))

        if len(hotels) == 1:
            axes = [axes]

        for ax, hotel in zip(axes, hotels):
            bars = ax.bar(booking_dist.columns, booking_dist.loc[hotel], color='skyblue')
            ax.set_xlabel('Τύπος Δωματίου')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Κατανομή Κρατήσεων ανά τύπο δωματίου για το {hotel}')
            ax.tick_params(axis='x', rotation=45)

            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}', 
                            xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(0, 3), 
                            textcoords="offset points", 
                            ha='center', va='bottom', rotation=0)

        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/room_type_distribution.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=2, column=0, columnspan=2, padx=1, pady=1)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=6, padx=1, pady=1, sticky='e')
    
    def plot_by_client(self, df):
        conditions = [
            (df['adults'] > 1) & (df['children'] + df['babies'] > 0),
            (df['adults'] > 1) & (df['children'] + df['babies'] == 0),
            (df['adults'] == 1) & (df['children'] + df['babies'] == 0)
        ]
        choices = ['Οικογένεια', 'Ζευγάρι', 'Μεμονωμένοι Ταξιδιώτες']
        df['customer_type'] = np.select(conditions, choices, default='Other')
        
        df = df[df['customer_type'] != 'Other']
        
        hotels = df['hotel'].unique()
        hotel1_stats = df[df['hotel'] == hotels[0]]['customer_type'].value_counts().sort_index()
        hotel2_stats = df[df['hotel'] == hotels[1]]['customer_type'].value_counts().sort_index()

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(11, 5))
        axes[0].bar(hotel1_stats.index, hotel1_stats.values, color='lightcoral')
        axes[0].set_xlabel('Τύπος Πελάτη')
        axes[0].set_ylabel('Αριθμός Κρατήσεων')
        axes[0].set_title(f'Κατανομή Κρατήσεων ανά τύπο πελάτη ({hotels[0]})')

        axes[1].bar(hotel2_stats.index, hotel2_stats.values, color='lightcoral')
        axes[1].set_xlabel('Τύπος Πελάτη')
        axes[1].set_ylabel('Αριθμός Κρατήσεων')
        axes[1].set_title(f'Κατανομή Κρατήσεων ανά τύπο πελάτη ({hotels[1]})')

        for ax in axes:
            for bar in ax.patches:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}', 
                            xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(0, 3), 
                            textcoords="offset points", 
                            ha='center', va='top', rotation=90)

        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/client_statistics.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=2, column=0, columnspan=2, padx=1, pady=1)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=6, padx=1, pady=1, sticky='e')


class BookingTrends(tk.Toplevel):
    def __init__(self, master, option, date_min, date_max):
        super().__init__(master)
        self.geometry('1200x800')
        self.option = option
        self.date_min = pd.to_datetime(date_min) if date_min else None
        self.date_max = pd.to_datetime(date_max) if date_max else None
        self.style = ttk.Style()
        self.style.configure('TButton', background='#EEEEEE', foreground='#373A40')
        self.create_widgets()

    def create_widgets(self):
        image_path = os.path.join(script_dir, "media/src/bg1.jpg")  
        image = Image.open(image_path)
        image = image.resize((1200, 800), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        connection = connect_to_db()
        df = pd.read_sql("SELECT * FROM bookings", connection)
        connection.close()

        df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-01')

        if isinstance(self.date_min, str):
            self.date_min = pd.to_datetime(self.date_min)
        if isinstance(self.date_max, str):
            self.date_max = pd.to_datetime(self.date_max)

        if self.date_min and self.date_max:
            df = df[(df['arrival_date'] >= self.date_min) & (df['arrival_date'] <= self.date_max)]
            timeInterval = f' από {self.date_min.strftime("%Y-%m-%d")} εώς {self.date_max.strftime("%Y-%m-%d")}'
        else:
            timeInterval = f'. '

        if self.option == 'μηνιαίες τάσεις':
            self.title(f'Τάσεις κρατήσεων ανά μήνα{timeInterval}')
            self.plot_by_month(df)
        elif self.option == 'ετήσιες τάσεις':
            self.title(f'Τάσεις κρατήσεων ανά έτος{timeInterval}')
            self.plot_by_year(df)
        elif self.option == 'εποχιακές τάσεις':
            self.title(f'Τάσεις κρατήσεων ανά εποχή{timeInterval}')
            self.plot_by_season(df)
        elif self.option == 'συγκριτικές τάσεις':
            self.geometry('1350x700')
            image = image.resize((1350, 700), Image.LANCZOS)
            hotels = df['hotel'].unique()
            hotel1, hotel2 = hotels[:2]
            self.title(f'Συγκριτική τάση μεταξύ των {hotel1}, {hotel2}{timeInterval}')
            self.plot_comparative(df)


    def plot_by_month(self, df):
        hotels = df['hotel'].unique()
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11, 7))
        # booking trends
        for ax, hotel in zip(axes[:, 0], hotels):
            monthly_bookings = df[df['hotel'] == hotel].groupby(df['arrival_date'].dt.to_period('M')).size()
            ax.plot(monthly_bookings.index.to_timestamp(), monthly_bookings.values, marker='o', linestyle='-', color='purple')
            ax.set_xticks(monthly_bookings.index.to_timestamp()[::3])  # Show fewer x-ticks
            ax.set_xticklabels(monthly_bookings.index.strftime('%b %Y')[::3], rotation=30, ha='right')
            ax.set_xlabel('Μήνας')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Κρατήσεις του ({hotel})')
        # cancellation trends
        for ax, hotel in zip(axes[:, 1], hotels):
            monthly_cancellations = df[df['hotel'] == hotel].groupby(df['arrival_date'].dt.to_period('M'))['is_canceled'].sum()
            ax.plot(monthly_cancellations.index.to_timestamp(), monthly_cancellations.values, marker='x', linestyle='--', color='red')
            ax.set_xticks(monthly_cancellations.index.to_timestamp()[::3])  # Show fewer x-ticks
            ax.set_xticklabels(monthly_cancellations.index.strftime('%b %Y')[::3], rotation=30, ha='right')
            ax.set_xlabel('Μήνας')
            ax.set_ylabel('Αριθμός Ακυρώσεων')
            ax.set_title(f'Ακυρώσεις του ({hotel})')
        # average booking length
        for ax, hotel in zip(axes[:, 2], hotels):
            avg_booking_length = df[df['hotel'] == hotel].groupby(df['arrival_date'].dt.to_period('M'))[['stays_in_weekend_nights', 'stays_in_week_nights']].mean().sum(axis=1)
            ax.plot(avg_booking_length.index.to_timestamp(), avg_booking_length.values, marker='s', linestyle='-', color='blue')
            ax.set_xticks(avg_booking_length.index.to_timestamp()[::3])  # Show fewer x-ticks
            ax.set_xticklabels(avg_booking_length.index.strftime('%b %Y')[::3], rotation=30, ha='right')
            ax.set_xlabel('Μήνας')
            ax.set_ylabel('Μέση διάρκεια παραμονής (νύχτες)')
            ax.set_title(f'Μέση διάρκεια παραμονής ({hotel})')
        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/monthly_booking_trends.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=2, padx=5, pady=5)


    def plot_by_year(self, df):
        hotels = df['hotel'].unique()
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11, 7))
        # booking trends
        for ax, hotel in zip(axes[:, 0], hotels):
            yearly_bookings = df[df['hotel'] == hotel].groupby('arrival_date_year').size()
            ax.plot(yearly_bookings.index, yearly_bookings.values, marker='o', linestyle='-', color='purple')
            ax.set_xticks(yearly_bookings.index)  # Show fewer x-ticks
            ax.set_xticklabels(yearly_bookings.index, rotation=30, ha='right')
            ax.set_xlabel('Έτος')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Κρατήσεις του ({hotel})')
        # cancellation trends
        for ax, hotel in zip(axes[:, 1], hotels):
            yearly_cancellations = df[df['hotel'] == hotel].groupby('arrival_date_year')['is_canceled'].sum()
            ax.plot(yearly_cancellations.index, yearly_cancellations.values, marker='x', linestyle='--', color='red')
            ax.set_xticks(yearly_cancellations.index)  # Show fewer x-ticks
            ax.set_xticklabels(yearly_cancellations.index, rotation=30, ha='right')
            ax.set_xlabel('Έτος')
            ax.set_ylabel('Αριθμός Ακυρώσεων')
            ax.set_title(f'Ακυρώσεις του ({hotel})')
        # average booking length
        for ax, hotel in zip(axes[:, 2], hotels):
            avg_booking_length = df[df['hotel'] == hotel].groupby('arrival_date_year')[['stays_in_weekend_nights', 'stays_in_week_nights']].mean().sum(axis=1)
            ax.plot(avg_booking_length.index, avg_booking_length.values, marker='s', linestyle='-', color='blue')
            ax.set_xticks(avg_booking_length.index)  # Show fewer x-ticks
            ax.set_xticklabels(avg_booking_length.index, rotation=30, ha='right')
            ax.set_xlabel('Έτος')
            ax.set_ylabel('Μέση διάρκεια παραμονής (νύχτες)')
            ax.set_title(f'Μέση διάρκεια παραμονής ({hotel})')
        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/yearly_booking_trends.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=2, padx=5, pady=5)


    def plot_by_season(self, df):
        season_map = {
            'January': 'Χειμώνας', 'February': 'Χειμώνας', 'March': 'Άνοιξη',
            'April': 'Άνοιξη', 'May': 'Άνοιξη', 'June': 'Καλοκαίρι',
            'July': 'Καλοκαίρι', 'August': 'Καλοκαίρι', 'September': 'Φθινόπωρο',
            'October': 'Φθινόπωρο', 'November': 'Φθινόπωρο', 'December': 'Χειμώνας'
        }
        df['season'] = df['arrival_date_month'].map(season_map)
        hotels = df['hotel'].unique()

        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11, 7))
        #  booking trends
        for ax, hotel in zip(axes[:, 0], hotels):
            seasonal_bookings = df[df['hotel'] == hotel].groupby('season').size()
            ax.plot(seasonal_bookings.index, seasonal_bookings.values, marker='o', linestyle='-', color='purple')
            ax.set_xticks(seasonal_bookings.index)  # Show fewer x-ticks
            ax.set_xticklabels(seasonal_bookings.index, rotation=30, ha='right')
            ax.set_xlabel('Εποχή')
            ax.set_ylabel('Αριθμός Κρατήσεων')
            ax.set_title(f'Κρατήσεις του ({hotel})')
        # cancellation trends
        for ax, hotel in zip(axes[:, 1], hotels):
            seasonal_cancellations = df[df['hotel'] == hotel].groupby('season')['is_canceled'].sum()
            ax.plot(seasonal_cancellations.index, seasonal_cancellations.values, marker='x', linestyle='--', color='red')
            ax.set_xticks(seasonal_cancellations.index)  # Show fewer x-ticks
            ax.set_xticklabels(seasonal_cancellations.index, rotation=30, ha='right')
            ax.set_xlabel('Εποχή')
            ax.set_ylabel('Αριθμός Ακυρώσεων')
            ax.set_title(f'Ακυρώσεις του ({hotel})')
        # average booking length
        for ax, hotel in zip(axes[:, 2], hotels):
            avg_booking_length = df[df['hotel'] == hotel].groupby('season')[['stays_in_weekend_nights', 'stays_in_week_nights']].mean().sum(axis=1)
            ax.plot(avg_booking_length.index, avg_booking_length.values, marker='s', linestyle='-', color='blue')
            ax.set_xticks(avg_booking_length.index)  # Show fewer x-ticks
            ax.set_xticklabels(avg_booking_length.index, rotation=30, ha='right')
            ax.set_xlabel('Εποχή')
            ax.set_ylabel('Μέση διάρκεια παραμονής (νύχτες)')
            ax.set_title(f'Μέση διάρκεια παραμονής ({hotel})')

        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/seasonal_booking_trends.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=2, padx=5, pady=5)


    def plot_comparative(self, df):
        hotels = df['hotel'].unique()

        hotel1, hotel2 = hotels[0], hotels[1]
        print(f"Comparing {hotel1} and {hotel2}")  # Debugging

        bookings_hotel1 = df[df['hotel'] == hotel1].groupby(df['arrival_date'].dt.to_period('M')).size()
        bookings_hotel2 = df[df['hotel'] == hotel2].groupby(df['arrival_date'].dt.to_period('M')).size()
        cancellations_hotel1 = df[df['hotel'] == hotel1].groupby(df['arrival_date'].dt.to_period('M'))['is_canceled'].sum()
        cancellations_hotel2 = df[df['hotel'] == hotel2].groupby(df['arrival_date'].dt.to_period('M'))['is_canceled'].sum()
        avg_nights_hotel1 = df[df['hotel'] == hotel1].groupby(df['arrival_date'].dt.to_period('M'))[['stays_in_weekend_nights', 'stays_in_week_nights']].mean().sum(axis=1)
        avg_nights_hotel2 = df[df['hotel'] == hotel2].groupby(df['arrival_date'].dt.to_period('M'))[['stays_in_weekend_nights', 'stays_in_week_nights']].mean().sum(axis=1)

        percentage_diff_bookings = ((bookings_hotel1 - bookings_hotel2) / bookings_hotel2) * 100
        percentage_diff_cancellations = ((cancellations_hotel1 - cancellations_hotel2) / cancellations_hotel2) * 100
        percentage_diff_avg_nights = ((avg_nights_hotel1 - avg_nights_hotel2) / avg_nights_hotel2) * 100

        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(13, 5))

        axes[0].plot(percentage_diff_bookings.index.to_timestamp(), percentage_diff_bookings.values, marker='o', linestyle='-', color='purple')
        axes[0].set_xticks(percentage_diff_bookings.index.to_timestamp()[::3])
        axes[0].set_xticklabels(percentage_diff_bookings.index.strftime('%b %Y')[::3], rotation=30, ha='right')
        axes[0].set_xlabel('Μήνας')
        axes[0].set_ylabel('Ποσοστιαία διαφορά (%)')
        axes[0].set_title('διαφορά% κρατήσεων')
        axes[1].plot(percentage_diff_cancellations.index.to_timestamp(), percentage_diff_cancellations.values, marker='x', linestyle='--', color='red')
        axes[1].set_xticks(percentage_diff_cancellations.index.to_timestamp()[::3])
        axes[1].set_xticklabels(percentage_diff_cancellations.index.strftime('%b %Y')[::3], rotation=30, ha='right')
        axes[1].set_xlabel('Μήνας')
        axes[1].set_ylabel('Ποσοστιαία διαφορά (%)')
        axes[1].set_title('διαφορά% ακυρώσεων')
        axes[2].plot(percentage_diff_avg_nights.index.to_timestamp(), percentage_diff_avg_nights.values, marker='s', linestyle='-', color='blue')
        axes[2].set_xticks(percentage_diff_avg_nights.index.to_timestamp()[::3])
        axes[2].set_xticklabels(percentage_diff_avg_nights.index.strftime('%b %Y')[::3], rotation=30, ha='right')
        axes[2].set_xlabel('Μήνας')
        axes[2].set_ylabel('Ποσοστιαία διαφορά (%)')
        axes[2].set_title('διαφορά% μέσης διάρκειας παραμονής')

        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/comparative_booking_trends.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=2, padx=5, pady=5)


class Seasonality(tk.Toplevel):
    def __init__(self, master, date_min, date_max):
        super().__init__(master)
        self.title("Εποχικότητα Κρατήσεων / Ακυρώσεων")
        self.geometry('1200x1000')
        self.date_min = pd.to_datetime(date_min) if date_min else None
        self.date_max = pd.to_datetime(date_max) if date_max else None
        self.style = ttk.Style()
        self.style.configure('TButton', background='#EEEEEE', foreground='#373A40')
        self.create_widgets()

    def create_widgets(self):
        image_path = os.path.join(script_dir, "media/src/bg1.jpg")  
        image = Image.open(image_path)
        image = image.resize((1200, 1000), Image.LANCZOS) 
        self.photo = ImageTk.PhotoImage(image)
        
        self.bg_label = tk.Label(self, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        connection = connect_to_db()
        df = pd.read_sql("SELECT * FROM bookings", connection)
        connection.close()
        
        df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-01')
        
        if isinstance(self.date_min, str):
            self.date_min = pd.to_datetime(self.date_min)
        if isinstance(self.date_max, str):
            self.date_max = pd.to_datetime(self.date_max)
        
        if self.date_min and self.date_max:
            df = df[(df['arrival_date'] >= self.date_min) & (df['arrival_date'] <= self.date_max)]
            timeInterval = f' από {self.date_min.strftime("%Y-%m-%d")} εώς {self.date_max.strftime("%Y-%m-%d")}'
        else:
            timeInterval = '. '
        self.title(f'Κατανομη Στατιστικών{timeInterval}')

        df['arrival_date_month'] = df['arrival_date'].dt.strftime('%B')

        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)

        hotels = df['hotel'].unique()

        fig, axs = plt.subplots(2, 2, figsize=(11, 7))

        # Plots Bookings x Cancelations for both hotels
        hotel_1_df = df[df['hotel'] == hotels[0]]
        seasonality_1 = hotel_1_df.groupby('arrival_date_month').agg({
            'hotel': 'count',
            'is_canceled': 'sum'
        }).reindex(month_order)
        axs[0, 0].plot(seasonality_1.index, seasonality_1['hotel'], color='seagreen', alpha=0.6, marker='*')
        axs[0, 0].set_title(f'Seasonality in Bookings for {hotels[0]}')
        axs[0, 0].set_xlabel('Month')
        axs[0, 0].set_ylabel('Number of Bookings')
        axs[0, 0].tick_params(axis='x', rotation=45)
        axs[0, 1].plot(seasonality_1.index, seasonality_1['is_canceled'], color='red', marker='o')
        axs[0, 1].set_title(f'Seasonality in Cancellations for {hotels[0]}')
        axs[0, 1].set_xlabel('Month')
        axs[0, 1].set_ylabel('Number of Cancellations')
        axs[0, 1].tick_params(axis='x', rotation=45)

        hotel_2_df = df[df['hotel'] == hotels[1]]
        seasonality_2 = hotel_2_df.groupby('arrival_date_month').agg({
            'hotel': 'count',
            'is_canceled': 'sum'
        }).reindex(month_order)
        axs[1, 0].plot(seasonality_2.index, seasonality_2['hotel'], color='seagreen', alpha=0.6, marker='*')
        axs[1, 0].set_title(f'Seasonality in Bookings for {hotels[1]}')
        axs[1, 0].set_xlabel('Month')
        axs[1, 0].set_ylabel('Number of Bookings')
        axs[1, 0].tick_params(axis='x', rotation=45)
        axs[1, 1].plot(seasonality_2.index, seasonality_2['is_canceled'], color='red', marker='o')
        axs[1, 1].set_title(f'Seasonality in Cancellations for {hotels[1]}')
        axs[1, 1].set_xlabel('Month')
        axs[1, 1].set_ylabel('Number of Cancellations')
        axs[1, 1].tick_params(axis='x', rotation=45)
        plt.tight_layout()

        plot_filename = os.path.join(script_dir, 'media/graphics/seasonality.png')
        plt.savefig(plot_filename)

        image = Image.open(plot_filename)
        photo = ImageTk.PhotoImage(image)

        plot_label = tk.Label(self, image=photo)
        plot_label.image = photo
        plot_label.grid(row=1, column=0, columnspan=2, padx=1, pady=1)

        back_button = ttk.Button(self, text="Back", command=self.destroy, style='TButton')
        back_button.grid(row=0, column=2, padx=1, pady=1, sticky='e')
        

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI_Window(root)
    root.mainloop()
