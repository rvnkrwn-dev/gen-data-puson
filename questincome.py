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


# Function to generate dummy data for Question
def generate_questions():
    questions = [
        "Saya memberikan anak makanan dengan menu seimbang (nasi, lauk, sayur, buah, dan susu).",
        "Saya memberikan anak makanan yang mengandung lemak (alpukat, kacang, daging, ikan, telur, susu).",
        "Saya memberikan anak makanan yang mengandung karbohidrat (nasi, umbi-umbian, jagung, tepung).",
        "Saya memberikan anak makanan yang mengandung protein (daging, ikan, kedelai, telur, kacang-kacangan, susu).",
        "Saya memberikan anak makanan yang mengandung vitamin (buah dan sayur).",
        "Jika saya tidak membimbing atau mengatur makan anak saya, dia akan makan terlalu banyak makanan cepat saji.",
        "Berapa banyak Anda mengawasi apa yang dimakan anak anda? Seperti permen, kue basah, es krim, snack kemasan, kue kering.",
        "Berapa banyak Anda mengawasi makanan ringan yang dimakan anak anda? Seperti: Snack jagung, snack kentang, kue kering, chiki-chiki.",
        "Seberapa Anda bertanggung jawab untuk memutuskan seberapa porsi makan anak anda?",
        "Saya memberikan anak saya makan dengan lauk nabati (tahu, tempe, dsb.) 2-3 potong.",
        "Anak saya tidak menghabiskan semua makanan yang ada di piring/mangkok setiap kali makan.",
        "Saya memberikan anak saya makan buah 2-3 potong.",
        "Saya memberikan makanan selingan 1-2 kali sehari diantara makanan utama.",
        "Anak saya tidak makan tepat waktu.",
        "Saya menyuapi makan anak saya tidak lebih dari 30 menit."
    ]

    for question_text in questions:
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO Question (question_text, createdAt, updatedAt) 
                VALUES (:question_text, :created_at, :updated_at)
                """
            ),
            {
                "question_text": question_text,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
    session.commit()


# Function to generate dummy data for Respon
def generate_responses():
    user_data = session.execute(text("SELECT id FROM User")).fetchall()
    question_data = session.execute(text("SELECT id FROM Question")).fetchall()
    med_check_up_data = session.execute(text("SELECT id FROM MedCheckUp")).fetchall()

    if not user_data:
        raise ValueError("No user records found in the database.")
    if not question_data:
        raise ValueError("No question records found in the database.")
    if not med_check_up_data:
        raise ValueError("No med check-up records found in the database.")

    answers = ["SL", "S", "J", "TP"]

    for med_check_up_id_tuple in med_check_up_data:
        med_check_up_id = med_check_up_id_tuple[0]
        for user_id_tuple in user_data:
            user_id = user_id_tuple[0]
            for question_id_tuple in question_data:
                question_id = question_id_tuple[0]
                answer = random.choice(answers)
                created_at = datetime.now()
                updated_at = datetime.now()
                session.execute(
                    text(
                        """
                        INSERT INTO Respon (user_id, quesion_id, med_check_up_id, answer, createdAt, updatedAt) 
                        VALUES (:user_id, :question_id, :med_check_up_id, :answer, :created_at, :updated_at)
                        """
                    ),
                    {
                        "user_id": user_id,
                        "question_id": question_id,
                        "med_check_up_id": med_check_up_id,
                        "answer": answer,
                        "created_at": created_at,
                        "updated_at": updated_at,
                    },
                )
    session.commit()


# Function to generate dummy data for IncomeLevel
def generate_income_levels():
    med_check_up_data = session.execute(text("SELECT id FROM MedCheckUp")).fetchall()

    if not med_check_up_data:
        raise ValueError("No med check-up records found in the database.")

    for med_check_up_id_tuple in med_check_up_data:
        med_check_up_id = med_check_up_id_tuple[0]
        monthly_income = random.uniform(500000, 10000000)
        child_expense = random.uniform(500000, 10000000)
        family_expense = random.uniform(500000, 10000000)
        dependents_count = random.randint(1, 5)
        social_assistance_received = random.uniform(0, 1000000)
        total_family_expense = family_expense + child_expense
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO IncomeLevel (monthly_income, child_expense, family_expense, dependents_count, social_assistance_received, total_family_expense, created_at, updated_at, med_check_up_id) 
                VALUES (:monthly_income, :child_expense, :family_expense, :dependents_count, :social_assistance_received, :total_family_expense, :created_at, :updated_at, :med_check_up_id)
                """
            ),
            {
                "monthly_income": monthly_income,
                "child_expense": child_expense,
                "family_expense": family_expense,
                "dependents_count": dependents_count,
                "social_assistance_received": social_assistance_received,
                "total_family_expense": total_family_expense,
                "created_at": created_at,
                "updated_at": updated_at,
                "med_check_up_id": med_check_up_id,
            },
        )
    session.commit()


# Generate data for Question, Respon, and IncomeLevel
generate_questions()
generate_responses()
generate_income_levels()

# Close the session
session.close()
