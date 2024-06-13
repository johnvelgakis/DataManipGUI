# Hotels Booking Data Analysis and Presentation GUI

## Project Description

This project is a graphical user interface (GUI) for analyzing and presenting hotel booking data. It provides various statistical analyses and visualizations, including basic statistics, booking distributions, trends, and seasonality. The GUI allows users to interact with the data, retrieve information from a MySQL database, and visualize results through various plots.

## Features

- **Basic Statistics**: Display average nights stayed, cancellation rates, and booking periods.
- **Booking Distribution**: Analyze booking distributions by month, season, room type, and customer type.
- **Trends**: Visualize monthly, yearly, and seasonal trends in bookings and cancellations.
- **Seasonality**: Explore seasonal patterns in bookings and cancellations.
- **Database Integration**: Retrieve and store data in a MySQL database.
- **Data Export**: Export analyzed data and database schema to CSV and SQL files.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the MySQL database:
    - Ensure MySQL is installed and running.
    - Create a database named `hotel_booking`.
    - Update the `db_connection.py` file with your MySQL credentials.
    - Import initial data into the database:
        ```sh
        python db_connection.py
        ```

## Usage

1. Launch the GUI:
    ```sh
    python main_menu.py
    ```

2. Use the main menu to navigate through different analysis options:
    - Basic Statistics
    - Booking Distribution
    - Trends
    - Seasonality

3. View and interact with the visualizations and data tables presented in each section.

4. To export analyzed data and database schema:
    ```sh
    python db_connection.py
    ```

5. Use the GUI controls to customize the analysis, such as selecting custom date ranges or different data groupings.

## Directory Structure

```
arxes_glwsswn/ 
│
├── main_menu.py
├── db_connection.py
├── hotel_booking.ipynb
├── README.MD
├── tables/
│   ├── basic_statistics.csv
│   ├── booking_distribution.csv
│   └── schema.sql
│
└── media/
    ├── src/
    │   └── bg1.jpg
    └── graphics/
        └── (All the plots being saved)
```

## Dependencies
 
- Python 3.x
- Tkinter
- pandas
- numpy
- matplotlib
- SQLAlchemy
- MySQL Connector
- PIL (Pillow)

Install the required dependencies using:
```sh
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please contact:

- **Ioannis Velgakis** - (Your email or contact information)
