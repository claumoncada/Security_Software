from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        Usuario.query.delete()
        usuario1 = Usuario(usuario='Clau', contraseña=generate_password_hash('12345'), rol='admin')
        usuario2 = Usuario(usuario='Sergy', contraseña=generate_password_hash('1234'))
        usuario3 = Usuario(usuario='Andres', contraseña=generate_password_hash('123'))
        usuario4 = Usuario(usuario='Ximena', contraseña=generate_password_hash('2310'))



        db.session.add(usuario1)
        db.session.add(usuario2)
        db.session.add(usuario3)
        db.session.add(usuario4)


        # Confirmar los cambios
        db.session.commit()

if __name__ == "__main__":
    init_db()


