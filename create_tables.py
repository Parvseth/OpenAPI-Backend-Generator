from db import Base, engine
from models import *  # Automatically import all models

print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
