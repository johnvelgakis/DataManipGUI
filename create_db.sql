CREATE DATABASE hotel_booking;

USE hotel_booking;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel VARCHAR(255),
    is_canceled INT,
    lead_time INT,
    arrival_date_year INT,
    arrival_date_month VARCHAR(255),
    arrival_date_week_number INT,
    arrival_date_day_of_month INT,
    stays_in_weekend_nights INT,
    stays_in_week_nights INT,
    adults INT,
    children FLOAT,
    babies INT,
    meal VARCHAR(255),
    country VARCHAR(255),
    market_segment VARCHAR(255),
    distribution_channel VARCHAR(255),
    is_repeated_guest INT,
    previous_cancellations INT,
    previous_bookings_not_canceled INT,
    reserved_room_type VARCHAR(255),
    assigned_room_type VARCHAR(255),
    booking_changes INT,
    deposit_type VARCHAR(255),
    agent FLOAT,
    company FLOAT,
    days_in_waiting_list INT,
    customer_type VARCHAR(255),
    adr FLOAT,
    required_car_parking_spaces INT,
    total_of_special_requests INT,
    reservation_status VARCHAR(255),
    reservation_status_date DATE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255),
    credit_card VARCHAR(255)
);

exit;
