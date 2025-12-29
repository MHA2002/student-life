# Student Life

## Video Demo
https://youtu.be/BBryBv9AKZ8

## Description
Student Life is a web application built with Flask that helps students manage their daily university life.
The goal of this project is to provide a single place where users can keep track of tasks, assignments,
notes, and birthdays.

The project requires users to register and log in. After logging in, each user can only see and manage
their own data. All information is stored in a SQLite database, and every table that contains user data
is linked to the logged-in user through a user_id.

This project was inspired by CS50 Finance, but instead of working with stocks, it focuses on productivity
and personal planning for students. I wanted to build something practical that I could actually use
in my daily life.

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
