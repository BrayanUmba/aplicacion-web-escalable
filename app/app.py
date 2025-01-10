from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define el modelo User con un nombre de tabla seguro
class User(db.Model):
    __tablename__ = 'users'  # Cambiamos el nombre de la tabla para evitar conflictos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # Crea las tablas si no existen al iniciar la aplicación
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
