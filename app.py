from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = "secret123"


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="flask_db"
    )


@app.route("/", methods=["GET", "POST"])
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
            session["user_id"] = user[0]
            session["name"] = user[1]
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    return render_template("dashboard.html", name=session["name"])


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/")

    return render_template("profile.html", name=session["name"])

@app.route("/courses")
def courses():
    if "user_id" not in session:
        return redirect("/")

    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM courses")
    data = cur.fetchall()

    con.close()

    return render_template("courses.html", courses=data)


@app.route("/help")
def help_page():
    if "user_id" not in session:
        return redirect("/")

    return render_template("help.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
