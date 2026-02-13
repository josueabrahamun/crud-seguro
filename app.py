from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

HTML = """
<!doctype html>
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-5">

<h2>CRUD Seguro</h2>

<form method="POST">
    <input class="form-control mb-2" name="nombre" placeholder="Nombre" required>
    <button class="btn btn-primary">Guardar</button>
</form>

<hr>

<table class="table table-bordered">
<tr>
<th>ID</th><th>Nombre</th><th>Acciones</th>
</tr>
{% for r in registros %}
<tr>
<td>{{r.id}}</td>
<td>{{r.nombre}}</td>
<td>
<a href="/delete/{{r.id}}" class="btn btn-danger btn-sm">Eliminar</a>

<button class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#edit{{r.id}}">
Editar
</button>

<div class="modal fade" id="edit{{r.id}}">
<div class="modal-dialog">
<div class="modal-content">
<form method="POST" action="/edit/{{r.id}}">
<div class="modal-header">
<h5 class="modal-title">Editar</h5>
</div>
<div class="modal-body">
<input class="form-control" name="nombre" value="{{r.nombre}}" required>
</div>
<div class="modal-footer">
<button class="btn btn-success">Guardar</button>
</div>
</form>
</div>
</div>
</div>

</td>
</tr>
{% endfor %}
</table>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")

        if len(nombre) > 100:
            return "Entrada demasiado larga"

        nuevo = Registro(nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()
        return redirect("/")

    registros = Registro.query.all()
    return render_template_string(HTML, registros=registros)

@app.route("/delete/<int:id>")
def delete(id):
    registro = Registro.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    registro = Registro.query.get_or_404(id)
    nombre = request.form.get("nombre")

    if len(nombre) > 100:
        return "Entrada demasiado larga"

    registro.nombre = nombre
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()

