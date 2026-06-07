from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Employee Dashboard</title>

<style>
body{
    font-family: Arial;
    background:#f4f4f4;
    padding:40px;
}

.container{
    max-width:900px;
    margin:auto;
}

.header{
    background:#1f2937;
    color:white;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
}

input{
    padding:10px;
    width:35%;
}

button{
    padding:10px 20px;
    border:none;
    border-radius:5px;
    cursor:pointer;
}

.add-btn{
    background:#22c55e;
    color:white;
}

.delete-btn{
    background:#ef4444;
    color:white;
}

table{
    width:100%;
    border-collapse:collapse;
}

th,td{
    padding:10px;
    border-bottom:1px solid #ddd;
}
</style>
</head>

<body>

<div class="container">

<div class="header">
<h1>Employee Management Dashboard</h1>
<p>AWS ECS + ECR + GitHub Actions CI/CD Demo</p>
<h2>Total Employees: {{ count }}</h2>
</div>

<div class="card">
<h2>Add Employee</h2>

<form method="POST" action="/add">
<input type="text" name="name" placeholder="Employee Name" required>
<input type="text" name="position" placeholder="Position" required>
<button class="add-btn">Add</button>
</form>
</div>

<div class="card">
<h2>Employee List</h2>

<table>
<tr>
<th>ID</th>
<th>Name</th>
<th>Position</th>
<th>Action</th>
</tr>

{% for employee in employees %}
<tr>
<td>{{ employee[0] }}</td>
<td>{{ employee[1] }}</td>
<td>{{ employee[2] }}</td>
<td>
<form method="POST" action="/delete/{{ employee[0] }}">
<button class="delete-btn">Delete</button>
</form>
</td>
</tr>
{% endfor %}

</table>
</div>

</div>
</body>
</html>
"""

def get_db():
    return sqlite3.connect("employees.db")

@app.route("/")
def home():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    conn.close()

    return render_template_string(
        HTML,
        employees=employees,
        count=len(employees)
    )

@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    position = request.form["position"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(name, position) VALUES (?, ?)",
        (name, position)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
