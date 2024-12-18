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

# Connect to the database using SQLAlchemy
DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URI, echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Daftar Puskesmas
puskesmas_list = [
    {
        "name": "Puskesmas Jatilawang",
        "address": "Desa Tuhjung",
        "phone": "(0281) 6848659",
    },
    {"name": "Puskesmas Lumbir", "address": "Jl. Raya Lumbir", "phone": "081391472978"},
    {"name": "Puskesmas Kebasen", "address": "Desa Kebasen", "phone": "(0281) 6847580"},
    {
        "name": "Puskesmas Kemranjen I",
        "address": "Desa Wijahan",
        "phone": "(0282) 5293286",
    },
    {
        "name": "Puskesmas Kemranjen II",
        "address": "Desa Buntu",
        "phone": "(0282) 5291332",
    },
    {
        "name": "Puskesmas Baturaden II",
        "address": "Desa Rempoah",
        "phone": "(0281) 681059",
    },
    {
        "name": "Puskesmas Kd.banteng",
        "address": "Desa Kedung Banteng No.380",
        "phone": "(0281) 7620781",
    },
    {
        "name": "Puskesmas Wangon I",
        "address": "Jl. Raya Wangon No. 59",
        "phone": "(0281) 7910767",
    },
    {
        "name": "Puskesmas Banyumas",
        "address": "Desa Sudagaran",
        "phone": "(0281) 796300",
    },
    {
        "name": "Puskesmas Patikraja",
        "address": "Jl. Raya Notog",
        "phone": "(0281) 6844892",
    },
    {"name": "Puskesmas Wangon 2", "address": "Desa Windunegara", "phone": "1234569"},
    {
        "name": "Puskesmas Rawalo",
        "address": "Jl. Raya Rawalo",
        "phone": "(0282) 6848090",
    },
    {
        "name": "Puskesmas Sumpiuh I",
        "address": "Desa Kebokura",
        "phone": "(0282) 497528",
    },
    {
        "name": "Puskesmas Sumpiuh II",
        "address": "Desa Kradenan",
        "phone": "(0282) 472472",
    },
    {
        "name": "Puskesmas Tambak I",
        "address": "Desa Kamulyan",
        "phone": "(0287) 472495",
    },
    {
        "name": "Puskesmas Tambak II",
        "address": "Desa Pesantren",
        "phone": "(0287) 472472",
    },
    {
        "name": "Puskesmas Pekuncen",
        "address": "Desa Banjaranyar",
        "phone": "(0281) 571729",
    },
    {
        "name": "Puskesmas Cilongok l",
        "address": "Desa Pernasidi",
        "phone": "(0281) 656286/655450",
    },
    {
        "name": "Puskesmas Somagede",
        "address": "Desa Somagede",
        "phone": "(0281) 796603",
    },
    {
        "name": "Puskesmas Kalibagor",
        "address": "Desa Kalibagor",
        "phone": "(0281) 6438207",
    },
    {"name": "Puskesmas Purwojati", "address": "Desa Purwojati", "phone": "1234567"},
    {
        "name": "Puskesmas Ajibarang l",
        "address": "Desa Ajibarang Wetan",
        "phone": "(0281) 7604056",
    },
    {
        "name": "Puskesmas Ajibarang II",
        "address": "Desa Kalibenda",
        "phone": "(0281) 572327",
    },
    {"name": "Puskesmas Gumelar", "address": "Desa Gumelar", "phone": "12"},
    {
        "name": "Puskesmas Cilongok II",
        "address": "Desa Jatisaba",
        "phone": "(0281) 7603948",
    },
    {
        "name": "Puskesmas Karanglewas",
        "address": "Desa Karang Kemiri",
        "phone": "(0281) 655754",
    },
    {
        "name": "Puskesmas Purwokerto Barat",
        "address": "Kelurahan Bantarsoka",
        "phone": "(0281) 639065",
    },
    {
        "name": "Puskesmas Purwokerto Utara l",
        "address": "Kelurahan Bancarkembar",
        "phone": "(0281) 626171",
    },
    {
        "name": "Puskesmas Purwokerto Utara II",
        "address": "Kelurahan Sumampir",
        "phone": "(0281) 639110",
    },
    {
        "name": "Puskesmas Purwokerto Selatan",
        "address": "Kelurahan Karang Klesem",
        "phone": "(0281) 6845019",
    },
    {
        "name": "Puskesmas Sokaraja l",
        "address": "Desa Sokaraja Wetan",
        "phone": "(0281) 6445141",
    },
    {
        "name": "Puskesmas Sokaraja II",
        "address": "Desa Banjarsari Kulon",
        "phone": "(0281) 6442204",
    },
    {
        "name": "Puskesmas Purwokerto Timur l",
        "address": "Kelurahan Mersi",
        "phone": "(0281) 633844",
    },
    {
        "name": "Puskesmas Purwokerto Timur II",
        "address": "Kelurahan Sokanegara",
        "phone": "(0281) 630591",
    },
    {
        "name": "Puskesmas Kembaran l",
        "address": "Desa Linggasari",
        "phone": "(0281) 7621216",
    },
    {"name": "Puskesmas Kembaran II", "address": "Desa Kramat", "phone": "123"},
    {"name": "Puskesmas Sumbang l", "address": "Desa Sumbang", "phone": "1234"},
    {"name": "Puskesmas Sumbang II", "address": "Desa Gandatapa", "phone": "12345"},
    {
        "name": "Puskesmas Baturaden l",
        "address": "Desa Kebumen",
        "phone": "(0281) 681026",
    },
]


# Custom function to generate puskesmas data using predefined list and user_id from database
def generate_puskesmas_data():
    # Ambil semua user_id dari tabel User
    user_ids = session.execute(text("SELECT id FROM User")).fetchall()
    if not user_ids:
        raise ValueError("No user records found in the database.")
    user_ids = [user_id[0] for user_id in user_ids]  # Convert to list of user_ids

    for puskesmas in puskesmas_list:
        user_id = random.choice(user_ids)  # Pilih user_id secara acak
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO Puskesmas (name, address, phone, user_id, created_at, updated_at) 
                VALUES (:name, :address, :phone, :user_id, :created_at, :updated_at)
                """
            ),
            {
                "name": puskesmas["name"],
                "address": puskesmas["address"],
                "phone": puskesmas.get("phone", ""),
                "user_id": user_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
    session.commit()


generate_puskesmas_data()

# Close the session
session.close()
