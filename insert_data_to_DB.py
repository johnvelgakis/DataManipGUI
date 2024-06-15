import pandas as pd
from db_connection import insert_booking_data

def main():
    data = pd.read_csv('hotel_booking.csv', sep=',')
    df = pd.DataFrame(data)
    insert_booking_data(df)

if __name__ == "__main__":
    main()
