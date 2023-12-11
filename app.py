from flask import Flask, render_template, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['RATELIMIT_LIMIT'] = '3 per minute'
app.config['RATELIMIT_KEY_FUNC'] = get_remote_address
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'  

limiter = Limiter(get_remote_address, app=app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), default='usuario')  

class RegistroAuditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    metodo = db.Column(db.String(50))
    hora = db.Column(db.DateTime, default=datetime.utcnow)
    nivel = db.Column(db.String(20))
    mensaje = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()

NIVEL_INFO = 'INFO'
NIVEL_ERROR = 'ERROR'

RUTA_LOGIN = 'login'
RUTA_CODIGO_GENERAL = 'index'
RUTA_VER_REGISTROS = 'ver_registros'
RUTA_ADMIN_DASHBOARD = 'admin_dashboard'  

@app.route(f'/{RUTA_LOGIN}', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="Has excedido el límite de solicitudes. Por favor, inténtalo de nuevo más tarde.")
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        usuario_existente = Usuario.query.filter_by(usuario=usuario).first()

        nivel_registro = NIVEL_INFO  

        if usuario_existente:
            if check_password_hash(usuario_existente.contraseña, contraseña):
                login_user(usuario_existente)
                return redirect(url_for(RUTA_CODIGO_GENERAL))
            else:
                nivel_registro = NIVEL_ERROR
        else:
            nivel_registro = NIVEL_ERROR

        nuevo_registro = RegistroAuditoria(
            usuario=usuario,
            metodo=request.method,
            nivel=nivel_registro,
            mensaje=f"Intento de inicio de sesión para el usuario {usuario}."
        )
        db.session.add(nuevo_registro)
        db.session.commit()

    return render_template('login.html', mensaje="")

@app.route(f'/{RUTA_CODIGO_GENERAL}')
@login_required
def index():
    print("Solicitud recibida en la ruta /index")
    return render_template('index.html')

@app.route(f'/{RUTA_VER_REGISTROS}', methods=['GET'])
@login_required
def ver_registros():
    registros = RegistroAuditoria.query.all()
    return render_template('ver_registros.html', registros=registros)

@app.route('/galeria', methods=['GET'])
@login_required
def galeria():
    return render_template('galeria.html')

@app.route('/sobrenosotros', methods=['GET'])
@login_required
def sobrenosotros():
    return render_template('sobrenosotros.html', methods=['GET'])

@app.route('/contacto', methods=['GET'])
@login_required
def contacto():
    return render_template('contacto.html')


@app.route('/miembro', methods=['GET'])
@login_required
def miembro():
    return render_template('members.html')

@app.route('/detalleoso')
@login_required
def detalleoso():
    return render_template('detalleoso.html')


@app.route(f'/{RUTA_ADMIN_DASHBOARD}')  
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        return redirect(url_for(RUTA_CODIGO_GENERAL))  

    return render_template('admin_dashboard.html', usuario=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(RUTA_LOGIN))

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))

