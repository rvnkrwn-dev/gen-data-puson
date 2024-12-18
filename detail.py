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

# Function to generate dummy DetailUser data based on Puskesmas locations
def generate_detail_user_data():
    user_data = session.execute(text("SELECT id FROM User")).fetchall()
    puskesmas_data = session.execute(text("SELECT id, address FROM Puskesmas")).fetchall()
    
    if not user_data:
        raise ValueError("No user records found in the database.")
    if not puskesmas_data:
        raise ValueError("No Puskesmas records found in the database.")
    
    puskesmas_mapping = {puskesmas_id: address for puskesmas_id, address in puskesmas_data}

    for user_id_tuple in user_data:
        user_id = user_id_tuple[0]
        puskesmas_id = random.choice(list(puskesmas_mapping.keys()))  # Pilih puskesmas_id secara acak
        address = puskesmas_mapping[puskesmas_id]
        phone = fake.phone_number()
        city = "Banyumas"  # Set semua city jadi Banyumas
        postalCode = fake.postcode()
        bod = fake.date_of_birth(minimum_age=18, maximum_age=70)
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO DetailUser (phone, address, city, postalCode, bod, user_id, created_at, updated_at) 
                VALUES (:phone, :address, :city, :postalCode, :bod, :user_id, :created_at, :updated_at)
                """
            ),
            {
                "phone": phone,
                "address": address,
                "city": city,
                "postalCode": postalCode,
                "bod": bod,
                "user_id": user_id,
                "created_at": created_at,
                "updated_at": updated_at
            },
        )
    session.commit()

# Generate data for DetailUser
generate_detail_user_data()

# Close the session
session.close()
