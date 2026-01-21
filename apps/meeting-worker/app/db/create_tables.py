from models import Base
from session import engine, DATABASE_URL

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set!")

Base.metadata.create_all(engine)
print("Tables created successfully!")