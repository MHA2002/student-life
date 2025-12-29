import os
from datetime import date, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = SQL("sqlite:///" + os.path.join(BASE_DIR, "life.db"))


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show detailed student dashboard"""
    user_id = session["user_id"]

    today = date.today()
    tasks_until = today + timedelta(days=3)
    assignments_until = today + timedelta(days=7)

    # Tasks
    due_tasks = db.execute(
        "SELECT id, title, due_date, is_done, created_at "
        "FROM tasks WHERE user_id = ? AND is_done = 0 AND due_date IS NOT NULL AND due_date <= ? "
        "ORDER BY due_date ASC",
        user_id, str(tasks_until)
    )
    overdue_tasks_count = db.execute(
        "SELECT COUNT(*) AS c FROM tasks WHERE user_id = ? AND is_done = 0 AND due_date IS NOT NULL AND due_date < ?",
        user_id, str(today)
    )[0]["c"]

    # Assignments
    due_assignments = db.execute(
        "SELECT id, course, title, due_date, priority, status, created_at "
        "FROM assignments WHERE user_id = ? AND status != 'done' AND due_date IS NOT NULL AND due_date <= ? "
        "ORDER BY due_date ASC",
        user_id, str(assignments_until)
    )
    overdue_assignments_count = db.execute(
        "SELECT COUNT(*) AS c FROM assignments WHERE user_id = ? AND status != 'done' AND due_date IS NOT NULL AND due_date < ?",
        user_id, str(today)
    )[0]["c"]

    # Notes (latest 3)
    latest_notes = db.execute(
        "SELECT id, title, body, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 3",
        user_id
    )

    # Birthdays (next 5)
    next_birthdays = db.execute(
        "SELECT id, name, month, day FROM birthdays WHERE user_id = ? ORDER BY month ASC, day ASC LIMIT 5",
        user_id
    )

    return render_template(
        "index.html",
        today=str(today),
        due_tasks=due_tasks,
        overdue_tasks_count=overdue_tasks_count,
        due_assignments=due_assignments,
        overdue_assignments_count=overdue_assignments_count,
        latest_notes=latest_notes,
        next_birthdays=next_birthdays
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirmation = request.form.get("confirmation", "")

    if not username:
        return apology("must provide username", 400)
    if not password:
        return apology("must provide password", 400)
    if password != confirmation:
        return apology("passwords must match", 400)

    pw_hash = generate_password_hash(password)

    try:
        new_id = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            pw_hash,
        )
    except ValueError:
        return apology("username already exists", 400)

    session.clear()
    session["user_id"] = new_id
    flash("Registered!")
    return redirect("/")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """Show tasks and allow adding/updating/deleting tasks"""

    user_id = session["user_id"]

    if request.method == "POST":
        action = request.form.get("action")

        # Add a new task
        if action == "add":
            title = request.form.get("title")
            due_date = request.form.get("due_date")  # format: YYYY-MM-DD or empty

            if not title:
                return apology("must provide task title", 400)

            db.execute(
                "INSERT INTO tasks (user_id, title, due_date) VALUES (?, ?, ?)",
                user_id,
                title.strip(),
                due_date if due_date else None
            )
            return redirect("/tasks")

        # Toggle done/undone
        elif action == "toggle":
            task_id = request.form.get("task_id")
            if not task_id:
                return apology("missing task id", 400)

            task = db.execute(
                "SELECT id, is_done FROM tasks WHERE id = ? AND user_id = ?",
                task_id,
                user_id
            )
            if len(task) != 1:
                return apology("task not found", 404)

            new_value = 0 if task[0]["is_done"] == 1 else 1
            db.execute(
                "UPDATE tasks SET is_done = ? WHERE id = ? AND user_id = ?",
                new_value,
                task_id,
                user_id
            )
            return redirect("/tasks")

        # Delete a task
        elif action == "delete":
            task_id = request.form.get("task_id")
            if not task_id:
                return apology("missing task id", 400)

            db.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                task_id,
                user_id
            )
            return redirect("/tasks")

        else:
            return apology("invalid action", 400)

    # GET: show all tasks
    tasks = db.execute(
        "SELECT id, title, due_date, is_done, created_at FROM tasks WHERE user_id = ? ORDER BY is_done ASC, due_date IS NULL, due_date ASC, created_at DESC",
        user_id
    )
    return render_template("tasks.html", tasks=tasks)


@app.route("/assignments", methods=["GET", "POST"])
@login_required
def assignments():
    """Show assignments and allow adding/updating/deleting"""

    user_id = session["user_id"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            course = request.form.get("course")
            title = request.form.get("title")
            due_date = request.form.get("due_date")
            priority = request.form.get("priority")

            if not course or not title:
                return apology("must provide course and title", 400)

            if priority not in ["low", "medium", "high"]:
                priority = "medium"

            db.execute(
                "INSERT INTO assignments (user_id, course, title, due_date, priority) VALUES (?, ?, ?, ?, ?)",
                user_id,
                course.strip(),
                title.strip(),
                due_date if due_date else None,
                priority
            )
            return redirect("/assignments")

        elif action == "status":
            assignment_id = request.form.get("assignment_id")
            new_status = request.form.get("status")

            if new_status not in ["todo", "doing", "done"]:
                return apology("invalid status", 400)

            db.execute(
                "UPDATE assignments SET status = ? WHERE id = ? AND user_id = ?",
                new_status,
                assignment_id,
                user_id
            )
            return redirect("/assignments")

        elif action == "delete":
            assignment_id = request.form.get("assignment_id")
            db.execute(
                "DELETE FROM assignments WHERE id = ? AND user_id = ?",
                assignment_id,
                user_id
            )
            return redirect("/assignments")

        return apology("invalid action", 400)

    assignments = db.execute(
        "SELECT id, course, title, due_date, priority, status, created_at FROM assignments WHERE user_id = ? ORDER BY due_date IS NULL, due_date ASC, created_at DESC",
        user_id
    )
    return render_template("assignments.html", assignments=assignments)


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    """Show notes and allow adding/deleting"""

    user_id = session["user_id"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            title = request.form.get("title")
            body = request.form.get("body")

            if not title or not body:
                return apology("must provide title and body", 400)

            db.execute(
                "INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
                user_id,
                title.strip(),
                body.strip()
            )
            return redirect("/notes")

        elif action == "delete":
            note_id = request.form.get("note_id")
            db.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", note_id, user_id)
            return redirect("/notes")

        return apology("invalid action", 400)

    notes = db.execute(
        "SELECT id, title, body, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC",
        user_id
    )
    return render_template("notes.html", notes=notes)


@app.route("/birthdays", methods=["GET", "POST"])
@login_required
def birthdays():
    """Show birthdays and allow adding/deleting"""

    user_id = session["user_id"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name")
            month = request.form.get("month")
            day = request.form.get("day")

            if not name or not month or not day:
                return apology("must provide name, month, and day", 400)

            try:
                month = int(month)
                day = int(day)
            except ValueError:
                return apology("month and day must be numbers", 400)

            if month < 1 or month > 12:
                return apology("invalid month", 400)

            if day < 1 or day > 31:
                return apology("invalid day", 400)

            db.execute(
                "INSERT INTO birthdays (user_id, name, month, day) VALUES (?, ?, ?, ?)",
                user_id,
                name.strip(),
                month,
                day
            )
            return redirect("/birthdays")

        elif action == "delete":
            birthday_id = request.form.get("birthday_id")
            db.execute(
                "DELETE FROM birthdays WHERE id = ? AND user_id = ?",
                birthday_id,
                user_id
            )
            return redirect("/birthdays")

        return apology("invalid action", 400)

    birthdays = db.execute(
        "SELECT id, name, month, day FROM birthdays WHERE user_id = ? ORDER BY month ASC, day ASC, name ASC",
        user_id
    )
    return render_template("birthdays.html", birthdays=birthdays)
