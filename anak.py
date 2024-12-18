import os
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from datetime import datetime, timedelta
import random

# Database configuration
DATABASE_USER = "pusonapp"
DATABASE_PASSWORD = quote_plus("Admin123!")
DATABASE_HOST = "15.235.202.96"
DATABASE_NAME = "pusonapp"

# Set the locale to Indonesian
fake = Faker("id_ID")

# Connect to the database using SQLAlchemy
DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URI, echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Tambahkan pengecekan untuk memastikan variabel lingkungan diambil dengan benar
if not DATABASE_HOST:
    raise ValueError(
        "DATABASE_HOST tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_USER:
    raise ValueError(
        "DATABASE_USER tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_PASSWORD:
    raise ValueError(
        "DATABASE_PASSWORD tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_NAME:
    raise ValueError(
        "DATABASE_NAME tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )

# Constants
GENDERS = ['male', 'female']
STATUSES = ['active', 'suspend', 'pending']

# Function to generate dummy Child data
def generate_child_data(child_count):
    user_ids = session.execute(text("SELECT id FROM User")).fetchall()
    posyandu_ids = session.execute(text("SELECT id FROM Posyandu")).fetchall()
    
    if not user_ids:
        raise ValueError("No user records found in the database.")
    if not posyandu_ids:
        raise ValueError("No posyandu records found in the database.")
    
    user_ids = [user_id[0] for user_id in user_ids]  # Convert to list of user_ids
    posyandu_ids = [posyandu_id[0] for posyandu_id in posyandu_ids]  # Convert to list of posyandu_ids

    for _ in range(child_count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"  # Kombinasikan nama depan dan belakang tanpa gelar
        bod = fake.date_of_birth(minimum_age=0, maximum_age=7)
        gender = random.choice(GENDERS)
        status = random.choice(STATUSES)
        user_id = random.choice(user_ids)  # Pilih user_id secara acak
        posyandu_id = random.choice(posyandu_ids)  # Pilih posyandu_id secara acak
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO Child (name, bod, gender, status, user_id, posyandu_id, created_at, updated_at) 
                VALUES (:name, :bod, :gender, :status, :user_id, :posyandu_id, :created_at, :updated_at)
                """
            ),
            {
                "name": name,
                "bod": bod,
                "gender": gender,
                "status": status,
                "user_id": user_id,
                "posyandu_id": posyandu_id,
                "created_at": created_at,
                "updated_at": updated_at
            },
        )
    session.commit()

# Generate data for Child
generate_child_data(child_count=350)

# Close the session
session.close()
