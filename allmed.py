import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import math
import logging

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

# Standar data tinggi, berat, dan lingkar kepala
standarTinggiBadan = {
    0: {"male": 49.4, "female": 48.6},
    1: {"male": 76.1, "female": 75.0},
    2: {"male": 85.5, "female": 84.5},
    3: {"male": 94.1, "female": 93.2},
    4: {"male": 102.4, "female": 101.4},
    5: {"male": 109.6, "female": 108.5},
    6: {"male": 116.3, "female": 115.0},
    7: {"male": 122.0, "female": 120.6},
}

standarBeratBadan = {
    0: {"male": 3.3, "female": 3.2},
    1: {"male": 10.2, "female": 9.8},
    2: {"male": 12.1, "female": 11.6},
    3: {"male": 14.0, "female": 13.5},
    4: {"male": 15.6, "female": 15.1},
    5: {"male": 17.1, "female": 16.5},
    6: {"male": 18.5, "female": 17.9},
    7: {"male": 19.9, "female": 19.2},
}

standarLingkarKepala = {
    0: {"male": 34.5, "female": 33.9},
    1: {"male": 46.0, "female": 45.4},
    2: {"male": 48.0, "female": 47.2},
    3: {"male": 49.5, "female": 48.6},
    4: {"male": 50.5, "female": 49.5},
    5: {"male": 51.3, "female": 50.3},
    6: {"male": 52.0, "female": 50.8},
    7: {"male": 52.5, "female": 51.2},
}

# Enum untuk StuntingStatus
class StuntingStatus:
    normal = "normal"
    stunting = "stunting"
    overweight = "overweight"
    obese = "obese"

# Fungsi menghitung IMT
def calculate_imt(weight, height):
    return weight / ((height / 100) ** 2)

# Fungsi menghitung IPB
def calculate_ipb(weight, circumference):
    return weight / circumference

# Fungsi memberikan variasi berdasarkan standar
def apply_variation(value, variation_type):
    if variation_type == "lebih":
        return round(value * 1.1, 2)  # 10% lebih tinggi
    elif variation_type == "sama":
        return round(value * (0.95 + 0.1 * random.random()), 2)  # dalam range ±5% dari nilai standar
    elif variation_type == "sedikit_beda":
        return round(value * 0.9, 2)  # 10% lebih rendah
    elif variation_type == "beda_jauh":
        return round(value * 0.8, 2)  # 20% lebih rendah
    return value

# Fungsi menentukan status stunting
def determine_stunting_status(age, gender, weight, height, circumference):
    age_floor = math.floor(age)
    imt = calculate_imt(weight, height)
    ipb = calculate_ipb(weight, circumference)
    height_standard = standarTinggiBadan[age_floor][gender]
    circumference_standard = standarLingkarKepala[age_floor][gender]

    if height < height_standard or imt < 18.5 or circumference < circumference_standard:
        return StuntingStatus.stunting
    elif imt >= 25 and imt < 30:
        return StuntingStatus.overweight
    elif imt >= 30:
        return StuntingStatus.obese
    else:
        return StuntingStatus.normal

# Fungsi menghitung umur
def calculate_age(birthdate):
    now = datetime.now()
    age = (now - birthdate).days / 365.25
    return round(age, 2)

# Fungsi generate data dengan proporsi yang seimbang
def generate_balanced_data(child_data, admin_posyandu_ids):
    results = []
    stunting_ratio = 0.3
    normal_ratio = 0.3
    overweight_ratio = 0.2
    obese_ratio = 0.2

    # Pastikan jumlah status sesuai dengan proporsi
    stunting_count = int(stunting_ratio * len(child_data))
    normal_count = int(normal_ratio * len(child_data))
    overweight_count = int(overweight_ratio * len(child_data))
    obese_count = int(obese_ratio * len(child_data))

    statuses = (
        [StuntingStatus.stunting] * stunting_count
        + [StuntingStatus.normal] * normal_count
        + [StuntingStatus.overweight] * overweight_count
        + [StuntingStatus.obese] * obese_count
    )
    random.shuffle(statuses)

    months = [
        "2023-01-", "2023-02-", "2023-03-", "2023-04-", "2023-05-", "2023-06-", "2023-07-",
        "2023-09-", "2023-10-", "2023-11-", "2023-12-", "2024-01-", "2024-02-", "2024-03-",
        "2024-04-", "2024-05-", "2024-06-", "2024-07-", "2024-09-", "2024-10-", "2024-11-", "2024-12-"
    ]

    for i, child in enumerate(child_data):
        gender = "male" if child[2] == "male" else "female"
        age = calculate_age(child[1])
        if age > 7:
            continue

        # Tentukan variasi berdasarkan kategori
        status = statuses[i % len(statuses)]
        height = apply_variation(standarTinggiBadan[math.floor(age)][gender], status)
        weight = apply_variation(standarBeratBadan[math.floor(age)][gender], status)
        circumference = apply_variation(
            standarLingkarKepala[math.floor(age)][gender], status
        )

        # Generate tanggal
        day = random.randint(1, 28)  # Untuk menghindari masalah di akhir bulan
        create_date = datetime.strptime(random.choice(months) + str(day), "%Y-%m-%d")
        update_date = create_date + timedelta(days=random.randint(1, 15))
        user_id = random.choice(admin_posyandu_ids)[0]

        # Hitung IMT dan IPB
        imt = calculate_imt(weight, height)
        ipb = calculate_ipb(weight, circumference)

        # Tambahkan data ke dalam results
        results.append(
            {
                "child_id": child[0],
                "height": height,
                "weight": weight,
                "age": age,
                "circumference": circumference,
                "created_at": create_date,
                "updated_at": update_date,
                "user_id": user_id,
                "status": status,
                "imt": imt,
                "ipb": ipb,
            }
        )
    return results

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mengambil data dari tabel Child dan User
child_data = session.execute(text("SELECT id, bod, gender FROM Child")).fetchall()
admin_posyandu_ids = session.execute(
    text("SELECT id FROM User WHERE role = 'admin_posyandu'")
).fetchall()

# Generate data
generated_data = generate_balanced_data(child_data, admin_posyandu_ids)

# Batch insert data ke tabel MedCheckUp dan ResultMedCheckUp
try:
    med_check_up_data = []
    result_med_check_up_data = []

    for data in generated_data:
        med_check_up_data.append(
            {
                "child_id": data["child_id"],
                "height": data["height"],
                "weight": data["weight"],
                "age": data["age"],
                "circumference": data["circumference"],
                "user_id": data["user_id"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
            }
        )

        result_med_check_up_data.append(
            {
                "imt": data["imt"],
                "ipb": data["ipb"],
                "status": data["status"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
            }
        )

    # Insert MedCheckUp data
    session.execute(
        text("""
            INSERT INTO MedCheckUp (child_id, height, weight, age, circumference, user_id, created_at, updated_at) 
            VALUES (:child_id, :height, :weight, :age, :circumference, :user_id, :created_at, :updated_at)
        """), med_check_up_data
    )

    # Insert ResultMedCheckUp data
    session.execute(
        text("""
            INSERT INTO ResultMedCheckUp (imt, ipb, status, created_at, updated_at) 
            VALUES (:imt, :ipb, :status, :created_at, :updated_at)
        """), result_med_check_up_data
    )

    session.commit()
    logger.info("Data berhasil dibuat dan dimasukkan ke tabel MedCheckUp dan ResultMedCheckUp")
except Exception as e:
    session.rollback()
    logger.error(f"Terjadi kesalahan saat memasukkan data: {e}")
