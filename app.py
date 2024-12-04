from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
import MySQLdb.cursors # type: ignore
from db import init_app, get_mysql

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializar la conexión a la base de datos
init_app(app)

# Ruta para la página principal de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        rol = request.form['rol']

        # Verificar usuario y contraseña en la base de datos
        mysql = get_mysql()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s', (usuario, contrasena))
        cuenta = cursor.fetchone()

        if cuenta:
            if rol == 'Administrativo' and cuenta['rol'] == 'Administrador':
                session['usuario'] = usuario
                return redirect(url_for('dashboard'))
            elif rol == 'Adjunto' and cuenta['rol'] == 'Empleado':
                session['usuario'] = usuario
                return redirect(url_for('adjunto_dashboard'))
            else:
                flash('Rol no válido para el usuario especificado')
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

# Ruta para el dashboard del administrador
@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        usuario = session['usuario']
        return render_template('admin_dashboard.html', usuario=usuario)
    else:
        return redirect(url_for('login'))

# Ruta para el dashboard del adjunto
@app.route('/adjunto_dashboard')
def adjunto_dashboard():
    if 'usuario' in session:
        usuario = session['usuario']
        return render_template('adjunto_dashboard.html', usuario=usuario)
    else:
        return redirect(url_for('login'))

# Ruta para probar la conexión a la base de datos
@app.route('/test_db')
def test_db():
    try:
        mysql = get_mysql()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result:
            return "Conexión exitosa a la base de datos"
        else:
            return "Conexión fallida"
    except Exception as e:
        return f"Error conectándose a la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True)