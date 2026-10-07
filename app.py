from flask import Flask, render_template, request, redirect
from datetime import date

from database import get_connection, init_db


app = Flask(__name__)


# =========================
# HOME / DASHBOARD
# =========================

@app.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor()

    # Pending tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 0"
    )
    pending_tasks = cursor.fetchone()[0]

    # Today's date
    today = date.today().isoformat()

    # Total expenses
    cursor.execute(
    "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )
    today_expenses = cursor.fetchone()[0]

    # Total study time
    cursor.execute(
    "SELECT COALESCE(SUM(duration), 0) FROM study_sessions"
    )
    today_study_minutes = cursor.fetchone()[0]

    # Pending grocery items
    cursor.execute(
        "SELECT COUNT(*) FROM groceries WHERE bought = 0"
    )
    grocery_items = cursor.fetchone()[0]

    # Total notes
    cursor.execute(
        "SELECT COUNT(*) FROM notes"
    )
    note_count = cursor.fetchone()[0]

    # Pending reminders
    cursor.execute(
        "SELECT COUNT(*) FROM reminders WHERE completed = 0"
    )
    upcoming_reminders = cursor.fetchone()[0]

    # Pending goals
    cursor.execute(
        "SELECT COUNT(*) FROM goals WHERE completed = 0"
    )
    pending_goals = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        today=today, 
        pending_tasks=pending_tasks,
        today_expenses=today_expenses,
        today_study_minutes=today_study_minutes,
        grocery_items=grocery_items,
        note_count=note_count,
        upcoming_reminders=upcoming_reminders,
        pending_goals=pending_goals
    )


# =========================
# TASKS
# =========================

@app.route("/tasks", methods=["GET", "POST"])
def tasks():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]

        cursor.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )

        connection.commit()

    cursor.execute(
        "SELECT id, title, completed FROM tasks"
    )

    task_list = cursor.fetchall()

    connection.close()

    return render_template(
        "tasks.html",
        tasks=task_list
    )


@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/tasks")

@app.route("/uncomplete/<int:task_id>")
def uncomplete_task(task_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = 0 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/tasks")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/tasks")


# =========================
# EXPENSES
# =========================

@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        expense_date = request.form["date"]

        cursor.execute(
            """
            INSERT INTO expenses
            (amount, category, description, date)
            VALUES (?, ?, ?, ?)
            """,
            (
                amount,
                category,
                description,
                expense_date
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY date DESC
        """
    )

    expense_list = cursor.fetchall()

    today = date.today().isoformat()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE date = ?
        """,
        (today,)
    )

    today_total = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "expenses.html",
        expenses=expense_list,
        today_total=today_total
    )

@app.route("/expenses/delete/<int:expense_id>")
def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/expenses")


# =========================
# STUDY
# =========================

@app.route("/study", methods=["GET", "POST"])
def study():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        subject = request.form["subject"]
        topic = request.form["topic"]
        duration = request.form["duration"]
        study_date = request.form["date"]

        cursor.execute(
            """
            INSERT INTO study_sessions
            (subject, topic, duration, date)
            VALUES (?, ?, ?, ?)
            """,
            (
                subject,
                topic,
                duration,
                study_date
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, subject, topic, duration, date
        FROM study_sessions
        ORDER BY date DESC
        """
    )

    study_list = cursor.fetchall()

    today = date.today().isoformat()

    cursor.execute(
        """
        SELECT COALESCE(SUM(duration), 0)
        FROM study_sessions
        WHERE date = ?
        """,
        (today,)
    )

    today_study_minutes = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "study.html",
        study_sessions=study_list,
        today_study_minutes=today_study_minutes
    )

@app.route("/study/delete/<int:study_id>")
def delete_study(study_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM study_sessions WHERE id = ?",
        (study_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/study")

# =========================
# GROCERY
# =========================

@app.route("/grocery", methods=["GET", "POST"])
def grocery():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        item = request.form["item"]
        quantity = request.form["quantity"]

        cursor.execute(
            """
            INSERT INTO groceries
            (item, quantity)
            VALUES (?, ?)
            """,
            (
                item,
                quantity
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, item, quantity, bought
        FROM groceries
        """
    )

    grocery_list = cursor.fetchall()

    connection.close()

    return render_template(
        "grocery.html",
        groceries=grocery_list
    )


@app.route("/grocery/bought/<int:grocery_id>")
def grocery_bought(grocery_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE groceries
        SET bought = 1
        WHERE id = ?
        """,
        (grocery_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/grocery")


@app.route("/grocery/delete/<int:grocery_id>")
def grocery_delete(grocery_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM groceries WHERE id = ?",
        (grocery_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/grocery")


# =========================
# NOTES
# =========================

@app.route("/notes", methods=["GET", "POST"])
def notes():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        note_date = date.today().isoformat()

        cursor.execute(
            """
            INSERT INTO notes
            (title, content, date)
            VALUES (?, ?, ?)
            """,
            (
                title,
                content,
                note_date
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, title, content, date
        FROM notes
        ORDER BY id DESC
        """
    )

    note_list = cursor.fetchall()

    connection.close()

    return render_template(
        "notes.html",
        notes=note_list
    )


@app.route("/notes/delete/<int:note_id>")
def delete_note(note_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/notes")


# =========================
# REMINDERS
# =========================

@app.route("/reminders", methods=["GET", "POST"])
def reminders():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        reminder_time = request.form["reminder_time"]

        cursor.execute(
            """
            INSERT INTO reminders
            (title, reminder_time)
            VALUES (?, ?)
            """,
            (
                title,
                reminder_time
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, title, reminder_time, completed
        FROM reminders
        ORDER BY reminder_time
        """
    )

    reminder_list = cursor.fetchall()

    connection.close()

    return render_template(
        "reminders.html",
        reminders=reminder_list
    )


@app.route("/reminders/complete/<int:reminder_id>")
def complete_reminder(reminder_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
        """,
        (reminder_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/reminders")


@app.route("/reminders/delete/<int:reminder_id>")
def delete_reminder(reminder_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/reminders")


# =========================
# GOALS
# =========================

@app.route("/goals", methods=["GET", "POST"])
def goals():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        target_date = request.form["target_date"]

        cursor.execute(
            """
            INSERT INTO goals
            (title, description, target_date)
            VALUES (?, ?, ?)
            """,
            (
                title,
                description,
                target_date
            )
        )

        connection.commit()

    cursor.execute(
        """
        SELECT id, title, description, target_date, completed
        FROM goals
        ORDER BY target_date
        """
    )

    goal_list = cursor.fetchall()

    connection.close()

    return render_template(
        "goals.html",
        goals=goal_list
    )


@app.route("/goals/complete/<int:goal_id>")
def complete_goal(goal_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE goals
        SET completed = 1
        WHERE id = ?
        """,
        (goal_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/goals")


@app.route("/goals/delete/<int:goal_id>")
def delete_goal(goal_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE id = ?",
        (goal_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/goals")


# =========================
# STATISTICS
# =========================

@app.route("/statistics")
def statistics():

    connection = get_connection()
    cursor = connection.cursor()

    # Total tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )
    total_tasks = cursor.fetchone()[0]

    # Completed tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    )
    completed_tasks = cursor.fetchone()[0]

    # Total expenses
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )
    total_expenses = cursor.fetchone()[0]

    # Total study time
    cursor.execute(
        "SELECT COALESCE(SUM(duration), 0) FROM study_sessions"
    )
    total_study_minutes = cursor.fetchone()[0]

    # Total grocery items
    cursor.execute(
        "SELECT COUNT(*) FROM groceries"
    )
    total_groceries = cursor.fetchone()[0]

    # Total notes
    cursor.execute(
        "SELECT COUNT(*) FROM notes"
    )
    total_notes = cursor.fetchone()[0]

    # Pending reminders
    cursor.execute(
        "SELECT COUNT(*) FROM reminders WHERE completed = 0"
    )
    pending_reminders = cursor.fetchone()[0]

    # Pending goals
    cursor.execute(
        "SELECT COUNT(*) FROM goals WHERE completed = 0"
    )
    pending_goals = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "statistics.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_expenses=total_expenses,
        total_study_minutes=total_study_minutes,
        total_groceries=total_groceries,
        total_notes=total_notes,
        pending_reminders=pending_reminders,
        pending_goals=pending_goals
    )


# =========================
# CALENDAR
# =========================

@app.route("/calendar")
def calendar():

    connection = get_connection()
    cursor = connection.cursor()

    # Get tasks
    cursor.execute(
        "SELECT id, title, completed FROM tasks"
    )
    tasks = cursor.fetchall()

    # Get expenses
    cursor.execute(
        "SELECT id, amount, category, date FROM expenses"
    )
    expenses = cursor.fetchall()

    # Get study sessions
    cursor.execute(
        """
        SELECT id, subject, topic, duration, date
        FROM study_sessions
        """
    )
    study_sessions = cursor.fetchall()

    # Get reminders
    cursor.execute(
        """
        SELECT id, title, reminder_time, completed
        FROM reminders
        """
    )
    reminders = cursor.fetchall()

    # Get goals
    cursor.execute(
        """
        SELECT id, title, target_date, completed
        FROM goals
        """
    )
    goals = cursor.fetchall()

    connection.close()

    return render_template(
        "calendar.html",
        tasks=tasks,
        expenses=expenses,
        study_sessions=study_sessions,
        reminders=reminders,
        goals=goals
    )

# =========================
# SETTINGS
# =========================

@app.route("/settings")
def settings():

    return render_template("settings.html")

# =========================
# REMINDER API
# =========================

@app.route("/api/reminders")
def reminder_api():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, reminder_time, completed
        FROM reminders
        """
    )

    reminders = cursor.fetchall()

    connection.close()

    reminder_data = []

    for reminder in reminders:

        reminder_data.append({
            "id": reminder[0],
            "title": reminder[1],
            "time": reminder[2],
            "completed": reminder[3]
        })

    return reminder_data


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":
    init_db()
    app.run(debug=True)