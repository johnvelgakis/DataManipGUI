import mysql.connector
import pandas as pd
import os
import subprocess

def connect_to_db():
    print("Connecting to MySQL database...")
    connection = mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="ArxesGlwsswn1!",  
        database="hotel_booking"
    )
    print("Connected to MySQL database!")
    return connection

def convert_nan_to_none(df):
    return df.applymap(lambda x: None if pd.isna(x) else x)

def insert_booking_data(df):
    df = convert_nan_to_none(df)
    connection = connect_to_db()
    cursor = connection.cursor()

    for index, row in df.iterrows():
        sql = """
        INSERT INTO bookings (
            hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month,
            arrival_date_week_number, arrival_date_day_of_month, stays_in_weekend_nights,
            stays_in_week_nights, adults, children, babies, meal, country,
            market_segment, distribution_channel, is_repeated_guest,
            previous_cancellations, previous_bookings_not_canceled, reserved_room_type,
            assigned_room_type, booking_changes, deposit_type, agent, company,
            days_in_waiting_list, customer_type, adr, required_car_parking_spaces,
            total_of_special_requests, reservation_status, reservation_status_date,
            name, email, phone_number, credit_card
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['hotel'], row['is_canceled'], row['lead_time'], row['arrival_date_year'], row['arrival_date_month'],
            row['arrival_date_week_number'], row['arrival_date_day_of_month'], row['stays_in_weekend_nights'],
            row['stays_in_week_nights'], row['adults'], 
            None if pd.isna(row['children']) else row['children'], 
            row['babies'], row['meal'], row['country'],
            row['market_segment'], row['distribution_channel'], row['is_repeated_guest'],
            row['previous_cancellations'], row['previous_bookings_not_canceled'], row['reserved_room_type'],
            row['assigned_room_type'], row['booking_changes'], row['deposit_type'], 
            None if pd.isna(row['agent']) else row['agent'], 
            None if pd.isna(row['company']) else row['company'], 
            row['days_in_waiting_list'], row['customer_type'], row['adr'], row['required_car_parking_spaces'],
            row['total_of_special_requests'], row['reservation_status'], row['reservation_status_date'],
            row['name'], row['email'], row.get('phone_number', None), row['credit_card']
        )

        # Debug
        print(f"Row index: {index}")
        print(f"SQL query: {sql}")
        print(f"Values: {values}")
        print(f"Number of placeholders in SQL: {sql.count('%s')}")
        print(f"Number of values provided: {len(values)}")

        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()

def retrieve_booking_data():
    connection = connect_to_db()
    query = """
    SELECT 
        hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month,
        arrival_date_week_number, arrival_date_day_of_month, stays_in_weekend_nights,
        stays_in_week_nights, adults, children, babies, meal, country,
        market_segment, distribution_channel, is_repeated_guest,
        previous_cancellations, previous_bookings_not_canceled, reserved_room_type,
        assigned_room_type, booking_changes, deposit_type, agent, company,
        days_in_waiting_list, customer_type, adr, required_car_parking_spaces,
        total_of_special_requests, reservation_status, reservation_status_date,
        name, email, phone_number, credit_card
    FROM bookings
    """
    
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df


def save_tables_to_csv(table_names, connection_params):
    """
    Save specified tables from a MySQL database to CSV files.

    Parameters:
    - table_names (list of str): List of table names to be saved.
    - connection_params (dict): Dictionary with connection parameters.
    """
    os.makedirs('tables', exist_ok=True)
    
    connection = mysql.connector.connect(**connection_params)
    
    for table in table_names:
        
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, connection)
        csv_path = os.path.join('tables', f"{table}.csv")
        
        df.to_csv(csv_path, index=False)
        
    connection.close()

def export_db_schema(connection_params):
    os.makedirs('tables', exist_ok=True)

    dump_command = (
        f"mysqldump --user={connection_params['user']} "
        f"--password={connection_params['password']} "
        f"--host={connection_params['host']} "
        f"--no-data {connection_params['database']} > tables/schema.sql"
    )
    subprocess.run(dump_command, shell=True, check=True)
    print("Database schema has been exported to 'tables/schema.sql'")


if __name__ == "__main__":
    connection_params = {
        'host': 'localhost',  
        'user': 'root',       
        'password': 'ArxesGlwsswn1!', 
        'database': 'hotel_booking'  
    }

    table_names = ['basic_statistics', 'booking_distribution']  
    save_tables_to_csv(table_names, connection_params)
    export_db_schema(connection_params)
