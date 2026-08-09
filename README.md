# Trekking-management-application
# Trekking Management Application

A simple web-based Trekking Management Application developed using Flask, SQLite, Jinja2, HTML, CSS, and Bootstrap.

The application helps trekking organizations manage treks, users, staff, and bookings through different role-based dashboards.

## Problem Statement

Trekking organizations often use spreadsheets, phone calls, and manual processes to manage trekking activities. This can make it difficult to manage trek availability, staff assignments, bookings, and trekking history.

This application provides a simple centralized system for managing these activities.

## Technologies Used

- Python
- Flask
- SQLite
- Flask-SQLAlchemy
- Jinja2
- HTML
- CSS
- Bootstrap

## User Roles

### Admin

The Admin can:

- View the admin dashboard
- Create treks
- Edit trek details
- Delete treks
- Approve trek staff
- Assign staff to treks
- View users and staff
- View bookings
- Manage trek information

### Trek Staff

Trek Staff can:

- Register and log in
- Access the dashboard after admin approval
- View assigned treks
- Update available slots
- Update trek status
- View participants registered for their treks

### User / Trekker

Users can:

- Register and log in
- View available treks
- Search and filter treks
- Book a trek
- View booking status
- View booking history
- Manage their profile

## Main Features

- Role-based login system
- User and staff registration
- Admin approval for staff
- Trek management
- Staff assignment
- Trek booking
- Prevention of overbooking
- Booking history
- Trek status management
- Search and filtering
- SQLite database
- Responsive Bootstrap interface

## Database

The application uses SQLite as the database.

The database is created programmatically when the Flask application is run.

Main tables include:

- `User`
- `Trek`
- `Booking`

## Project Structure

```text
Trekking_Management/
│
├── app.py 
├── config.py
├── file1.py
|
│
├── folder2/
│   ├── __init__.py
│   └── models.py
|   |── forms.py
|   |── auth.py
|   |── utils.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── staff_dashboard.html
│   ├── user_dashboard.html
│   ├── add_trek.html
│   ├── view_treks.html
│   └── bookings.html
│
├── static/
│   └── css/
│       └── style.css
│
└── project_report
