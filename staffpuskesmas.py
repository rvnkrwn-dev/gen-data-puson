import os
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from datetime import datetime
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


# Function to generate StaffPuskesmas data based on users with role 'admin_puskesmas'
def generate_staff_puskesmas_data():
    puskesmas_ids = session.execute(text("SELECT id FROM Puskesmas")).fetchall()
    user_data = session.execute(
        text("SELECT id, full_name FROM User WHERE role = 'admin_puskesmas'")
    ).fetchall()

    if not user_data:
        raise ValueError("No admin_puskesmas user records found in the database.")

    for user_id, full_name in user_data:
        puskesmas_id = random.choice(puskesmas_ids)[0]  # Pilih puskesmas_id secara acak
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO StaffPuskesmas (name, user_id, puskesmas_id, created_at, updated_at) 
                VALUES (:name, :user_id, :puskesmas_id, :created_at, :updated_at)
                """
            ),
            {
                "name": full_name,
                "user_id": user_id,
                "puskesmas_id": puskesmas_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
    session.commit()


generate_staff_puskesmas_data()

# Close the session
session.close()
