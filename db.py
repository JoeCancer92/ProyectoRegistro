from flask_mysqldb import MySQL # type: ignore

mysql = None

def init_app(app):
    global mysql
    # Configuración de MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '123456'
    app.config['MYSQL_DB'] = 'SistemaRegistroMSB'
    
    mysql = MySQL(app)

def get_mysql():
    return mysql
