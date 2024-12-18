from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

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

# List of tables to truncate
tables = [
    'User',
    'StaffPuskesmas',
    'StaffPosyandu',
    'ResultMedCheckUp',
    'RefreshToken',
    'Puskesmas',
    'Posyandu',
    'Notification',
    'NIKChild',
    'NIK',
    'MedCheckUp',
    # 'Log',
    'KK',
    'DetailUser',
    'Child',
    'ResultMedCheckUp',
    'Question',
    'Respon',
    'IncomeLevel'
]

def truncate_tables():
    try:
        # Disable foreign key checks
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Truncate each table
        for table in tables:
            session.execute(text(f'TRUNCATE TABLE {table}'))
            print(f'Table {table} truncated successfully.')
        
        # Enable foreign key checks
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    truncate_tables()
