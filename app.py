from flask import Flask, Markup, redirect, render_template, request, session
from sqlite3 import connect

app = Flask(__name__)
app.secret_key = "freddy's dungeon"

with connect("database.db") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students(name text, class text);")
    conn.commit()

@app.route("/") #This is a decorator, a python feature to modify functions
def root():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    session["user"] = username
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user")
    return redirect("/")

@app.route("/data", methods=["POST"])
def data():
    name = request.form["name"]
    clss = request.form["class"] #Not a typo, class is a reserved keyword
    with connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, class) VALUES (?, ?);", (name, clss))
        conn.commit()
    return render_template("data.html", name=name, clss=clss)

@app.route("/database") #More advanced example, takes data from database and dynamically generates page
def database():
    with connect("database.db") as conn:
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM students;").fetchall()
    database = ""
    for student in data:
        database += """
            <tr>
                <td>{name}</td>
                <td>{clss}</td>
            </tr>
        """.format(name=student[0], clss=student[1])
    return render_template("database.html", database=Markup(database))

@app.route("/<page_name>") #This is a wildcard route which is useful for making a large website
def page(page_name):
    try:
        return render_template(page_name + ".html")
    except:
        return redirect("/")

app.run(debug=True) #Run the app with "python app.py", go to 127.0.0.1:5000 in your browser