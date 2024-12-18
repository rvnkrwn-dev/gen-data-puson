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

# Custom list of desa names in Kabupaten Banyumas, Provinsi Jawa Tengah
desa_names = [
    "Desa Binangun",
    "Desa Danaraja",
    "Desa Dawuhan",
    "Desa Kalisube",
    "Desa Karangrau",
    "Desa Kedunggede",
    "Desa Kedunguter",
    "Desa Pekunden",
    "Desa Sudagaran",
    "Desa Rempoah",
    "Desa Tuhjung",
    "Desa Lumbir",
    "Desa Kebasen",
    "Desa Wijahan",
    "Desa Buntu",
    "Desa Kedung Banteng",
    "Desa Windunegara",
    "Desa Rawalo",
    "Desa Kebokura",
    "Desa Kradenan",
    "Desa Kamulyan",
    "Desa Pesantren",
    "Desa Banjaranyar",
    "Desa Pernasidi",
    "Desa Somagede",
    "Desa Kalibagor",
    "Desa Purwojati",
    "Desa Ajibarang Wetan",
    "Desa Kalibenda",
    "Desa Gumelar",
    "Desa Jatisaba",
    "Desa Karang Kemiri",
    "Desa Bancarkembar",
    "Desa Sumampir",
    "Desa Karang Klesem",
    "Desa Sokaraja Wetan",
    "Desa Banjarsari Kulon",
    "Desa Linggasari",
    "Desa Kramat",
    "Desa Sumbang",
    "Desa Gandatapa",
    "Desa Kebumen",
]


# Function to generate dummy Posyandu data
def generate_posyandu_data(posyandu_count):
    puskesmas_ids = session.execute(text("SELECT id FROM Puskesmas")).fetchall()
    user_ids = session.execute(text("SELECT id FROM User")).fetchall()

    if not user_ids:
        raise ValueError("No user records found in the database.")

    user_ids = [user_id[0] for user_id in user_ids]  # Convert to list of user_ids

    for puskesmas_id_tuple in puskesmas_ids:
        puskesmas_id = puskesmas_id_tuple[0]
        used_names = set()  # Set to keep track of used names for uniqueness

        for j in range(posyandu_count):
            # Generate a unique Posyandu name by combining desa name with a random identifier
            while True:
                base_name = fake.random_element(elements=desa_names)
                suffix = fake.random_int(1, 99)
                posyandu_name = f"{base_name} Posyandu {suffix}"

                if posyandu_name not in used_names:
                    used_names.add(posyandu_name)
                    break  # Exit loop once a unique name is generated

            posyandu_address = f"Jl. {fake.street_name()}, {base_name}, Banyumas"
            posyandu_phone = fake.phone_number()
            user_id = random.choice(user_ids)  # Pilih user_id secara acak
            created_at = datetime.now()
            updated_at = datetime.now()
            session.execute(
                text(
                    """
                    INSERT INTO Posyandu (name, address, phone, user_id, puskesmas_id, created_at, updated_at) 
                    VALUES (:name, :address, :phone, :user_id, :puskesmas_id, :created_at, :updated_at)
                    """
                ),
                {
                    "name": posyandu_name,
                    "address": posyandu_address,
                    "phone": posyandu_phone,
                    "user_id": user_id,
                    "puskesmas_id": puskesmas_id,
                    "created_at": created_at,
                    "updated_at": updated_at,
                },
            )
        session.commit()


# Generate data for 5 Posyandu per Puskesmas
generate_posyandu_data(posyandu_count=5)

# Close the session
session.close()
