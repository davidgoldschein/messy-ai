from app import create_app
from models import db

app = create_app()

def init_db():
    with app.app_context():
        print("Ensuring database tables are created...")
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
