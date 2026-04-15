import pymysql
from app.core.config import settings
from sqlalchemy import create_engine

def create_database():
    # Parse the connection string to get host, user, password
    # format: mysql+pymysql://root:Mithun1701@localhost:3306/carbon_db
    url = settings.DATABASE_URL
    base_url = url.split("/")[0] + "//" + url.split("//")[1].split("/")[0]
    db_name = url.split("/")[-1]
    
    from sqlalchemy import text
    # Connect to MySQL server (not the DB)
    engine = create_engine(base_url)
    with engine.connect() as conn:
        print(f"Ensuring database '{db_name}' exists...")
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()
        print("Database checked/created.")

if __name__ == "__main__":
    create_database()
