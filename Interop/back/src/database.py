from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your own PostgreSQL instance
DATABASE_URL = 'postgresql://admin:password@localhost:5432/sante_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
