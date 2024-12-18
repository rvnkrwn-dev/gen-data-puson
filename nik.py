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


# Function to generate dummy NIK data for each KK
def generate_nik_data_for_all_kk():
    kk_data = session.execute(text("SELECT id, user_id FROM KK")).fetchall()

    if not kk_data:
        raise ValueError("No KK records found in the database.")

    for kk_id, user_id in kk_data:
        number = fake.unique.numerify(text="##########")  # Generate random NIK number
        url_ktp = None
        secure_url_ktp = None
        public_id_ktp = None
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO NIK (number, url_ktp, secure_url_ktp, public_id_ktp, user_id, kk_id, created_at, updated_at) 
                VALUES (:number, :url_ktp, :secure_url_ktp, :public_id_ktp, :user_id, :kk_id, :created_at, :updated_at)
                """
            ),
            {
                "number": number,
                "url_ktp": url_ktp,
                "secure_url_ktp": secure_url_ktp,
                "public_id_ktp": public_id_ktp,
                "user_id": user_id,
                "kk_id": kk_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
    session.commit()


# Generate data for all KK
generate_nik_data_for_all_kk()

# Close the session
session.close()
