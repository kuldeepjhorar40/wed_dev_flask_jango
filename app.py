import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "secret123")


# ------------------------
# Database Connection
# ------------------------
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DB", "flask_db"),
        cursorclass=pymysql.cursors.DictCursor
    )


# ------------------------
# Login
# ------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        con = get_db_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()
        con.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["name"]

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        con = get_db_connection()
        cur = con.cursor()

        # Check if email exists
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()

        if existing:
            flash("Email already registered", "warning")
            return redirect("/register")

        # Insert user
        cur.execute(
            "INSERT INTO users(username, email, password) VALUES(%s,%s,%s)",
            (username, email, password)
        )

        con.commit()
        con.close()

        flash("Registration successful. Login now.", "success")
        return redirect("/login")

    return render_template("register.html")


# ------------------------
# Dashboard
# ------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# ------------------------
# Profile
# ------------------------
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()

    con.close()

    return render_template("profile.html", user=user)


# ------------------------
# Courses
# ------------------------
@app.route("/courses")
def courses():

    if "user_id" not in session:
        return redirect("/login")

    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    con.close()

    return render_template("courses.html", courses=courses)


# ------------------------
# Help
# ------------------------
@app.route("/help")
def help_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("help.html")


# ------------------------
# Logout
# ------------------------
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# ------------------------
# Run App
# ------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
