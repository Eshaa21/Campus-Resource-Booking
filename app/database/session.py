
from database.connection import SessionLocal
#Why do we need this? It opens a database session for an API request and closes it afterward.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
