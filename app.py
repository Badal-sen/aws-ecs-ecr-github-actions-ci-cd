from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Sarah Johnson", "position": "Manager"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management System</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body{
            background:#f5f7fb;
        }

        .hero{
            background:#212529;
            color:white;
            padding:30px;
            border-radius:15px;
            margin-bottom:20px;
        }

        .card{
            border:none;
            border-radius:15px;
            box-shadow:0 4px 12px rgba(0,0,0,.1);
        }
    </style>
</head>

<body>

<div class="container mt-5">

    <div class="hero">
        <h1>Employee Management Dashboard</h1>
        <p>AWS ECS + ECR + GitHub Actions CI/CD Demo</p>
        <h4>Total Employees: {{ employees|length }}</h4>
    </div>

    <div class="card p-4 mb-4">

        <h4>Add Employee</h4>

        <form method="POST" action="/add">

            <div class="row">

                <div class="col-md-5">
                    <input class="form-control"
                           type="text"
                           name="name"
                           placeholder="Employee Name"
                           required>
                </div>

                <div class="col-md-5">
                    <input class="form-control"
                           type="text"
                           name="position"
                           placeholder="Position"
                           required>
                </div>

                <div class="col-md-2">
                    <button class="btn btn-success w-100"
                            type="submit">
                        Add
                    </button>
                </div>

            </div>

        </form>

    </div>

    <div class="card p-4">

        <h4>Employee List</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Position</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>

            {% for employee in employees %}

                <tr>

                    <td>{{ employee.id }}</td>
                    <td>{{ employee.name }}</td>
                    <td>{{ employee.position }}</td>

                    <td>

                        <form method="POST"
                              action="/delete/{{ employee.id }}">

                            <button class="btn btn-danger btn-sm">
                                Delete
                            </button>

                        </form>

                    </td>

                </tr>

            {% endfor %}

            </tbody>

        </table>

    </div>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, employees=employees)

@app.route("/add", methods=["POST"])
def add():
    employees.append({
        "id": len(employees) + 1,
        "name": request.form["name"],
        "position": request.form["position"]
    })
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    global employees
    employees = [e for e in employees if e["id"] != id]
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)