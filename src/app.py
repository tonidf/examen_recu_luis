from ast import Mod
from flask import Flask, render_template, url_for, redirect, request
from config import config
from flask_mysqldb import MySQL
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from entities.ModelUser import ModelUser

app = Flask(__name__)

db = MySQL(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def get_by_id(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def welcome():
    
    return render_template('welcome.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        ModelUser.register(db,username, password)

        logged_user = ModelUser.login(db, username, password)

        login_user(logged_user)

        if logged_user.username == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('pretienda'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        logged_user = ModelUser.login(db, username, password)


        if logged_user:
            if logged_user.password:
                if logged_user.username == 'admin':
                    print('sesion iniciada como admin')
                    return redirect(url_for('admin'))
                    
                print('Sesion iniciada')
                return redirect(url_for('pretienda'))
            else:
                print('Contraseña incorrecta')
                return redirect(url_for('register'))
        else:
            print("Usuario no encontrado")
    else:
        if current_user.is_authenticated:
            return redirect(url_for('pretienda'))
        return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    
    return render_template('admin.html', usuario=current_user.is_authenticated)

@app.route('/productos')
@login_required
def productos():

    productos = ModelUser.get_productos(db)
    return render_template('productos.html', productos=productos)

@app.route('/add_product', methods=['POST', 'GET'])
@login_required
def add_product():
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        foto = request.form.get('foto')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')
        descripcion = request.form.get('nombre')

        ModelUser.add_producto(db, nombre, cantidad, precio, descripcion, foto)

        return redirect(url_for('productos'))
    else:
        return render_template('add_product.html')
    
@app.route('/delete_product/<string:id>')
@login_required
def delete_product(id):

    ModelUser.delete_product(db, id)
    return redirect(url_for('productos'))

@app.route('/edit_product/<string:id>')
@login_required
def edit_product(id):
    
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = %s ', (id,))
    data = cursor.fetchone()
    return render_template('edit_product.html',producto=data)

@app.route('/update_product/<string:id>', methods=['POST'])
@login_required
def update_product(id):
    nombre = request.form.get('nombre')
    foto = request.form.get('foto')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    descripcion = request.form.get('nombre')

    cursor = db.connection.cursor()
    cursor.execute('UPDATE productos SET nombre = %s, precio = %s, descripcion = %s, cantidad = %s, foto = %s WHERE id = %s', (nombre, precio, descripcion, cantidad, foto, id))
    db.connection.commit()

    return redirect(url_for('productos'))

@app.route('/pretienda')
def pretienda():
    render_template('pretienda.html', nombre=current_user.username)

@app.route('/tienda')
def tienda():
    productos = ModelUser.get_productos(db)
    return render_template('tienda.html', productos=productos)



@app.route('/usuarios')
def usuarios():
    return "<h1> Usuarios </h1>"



if __name__ == '__main__':

    app.config.from_object(config['development'])
    app.run()