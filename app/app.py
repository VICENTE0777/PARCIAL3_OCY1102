from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "clave_super_segura"

def db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = escape(request.form["username"])
        password = request.form["password"]

        conn = db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciales inválidas")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = db()
    tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (session["user_id"],)).fetchall()

    return render_template("dashboard.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))

    task = escape(request.form["task"])

    conn = db()
    conn.execute("INSERT INTO tasks (user_id, task) VALUES (?,?)", (session["user_id"], task))
    conn.commit()

    return redirect(url_for("dashboard"))


@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()

    if task["user_id"] != session["user_id"]:
        return "No autorizado", 403

    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
