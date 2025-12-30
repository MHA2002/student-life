# Student Life

## Video Demo
https://youtu.be/BBryBv9AKZ8

## Description
Student Life is a Flask web application that helps students organize their university life in one place.
Many students track deadlines in different places (notes apps, calendars, chat messages, or even paper),
so the main goal of this project is to provide a simple and clear dashboard for daily planning.

The application supports user accounts. A user can register, log in, and log out. Passwords are stored securely
using hashing, and sessions are managed with Flask-Session. After logging in, each user can only see and manage
their own data. This is done by linking every record in the database to the current user through a user_id.

The app has four main features:
Tasks, Assignments, Notes, and Birthdays. In the Tasks page, users can add tasks with an optional due date,
mark tasks as Done or Todo, and delete tasks. Each task also shows the time it was created (“added at …”),
which makes it easier to track what was recently added.

In the Assignments page, users can add an assignment with the course name, a title, an optional due date,
and a priority level (low, medium, or high). Assignments can also be updated by status (todo, doing, or done),
and deleted when they are no longer needed. Notes allow users to store short text reminders or study points.
Birthdays allow users to save important dates and see upcoming birthdays.

A small but important usability improvement is done using JavaScript: tasks and assignments with due dates
are highlighted automatically. Overdue items are shown with a stronger highlight and items due soon are
highlighted differently, helping students focus on urgent work quickly.

This project was inspired by CS50 Finance in terms of structure (Flask routes, templates, SQL queries, and
login system), but it solves a different real-life problem: personal student planning and productivity.

## Features
- User registration and login with password hashing
- Task management with optional due dates
- Ability to mark tasks as done or delete them
- Assignment tracking with course name, priority, and status
- Personal notes
- Birthday reminders
- A dashboard that shows upcoming deadlines and recent information

## Files
- app.py: The main Flask application that handles routing and logic
- helpers.py: Contains helper functions such as login_required and apology
- schema.sql: Defines the database schema
- life.db: SQLite database file
- templates/: HTML templates for the application
- static/: CSS and JavaScript files

## Design Choices
I chose to separate the application into multiple pages (Tasks, Assignments, Notes, and Birthdays)
to keep each feature simple and easy to use. A dashboard was added to give users a quick overview
after logging in.

JavaScript was used to highlight overdue and upcoming deadlines to improve usability and help users
focus on urgent items.

## Conclusion
This project helped me practice Flask, SQL, authentication, sessions, and front-end templating.
It represents what I learned throughout CS50 and how I can apply it to build a real web application.
