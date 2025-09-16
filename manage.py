from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import click, os

app = create_app()

@app.cli.command("create_admin_if_needed")
def create_admin_if_needed():
    email = os.getenv("ADMIN_EMAIL", "admin@cryptolab.local")
    name = os.getenv("ADMIN_NAME", "Admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    if not User.query.filter_by(email=email).first():
        u = User(email=email, name=name, is_admin=True,
                 password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        click.echo(f"[OK] Admin user created: {email}")
    else:
        click.echo("[OK] Admin already exists")
