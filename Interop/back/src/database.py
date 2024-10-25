from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# Replace with your own PostgreSQL instance
DATABASE_URL = 'postgresql://admin:password@db/sante_db'

engine = create_engine(DATABASE_URL,
                       poolclass=QueuePool,
                       pool_size=5,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_pre_ping=True
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
