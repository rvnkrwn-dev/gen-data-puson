import subprocess

# Daftar file Python yang ingin dijalankan dalam urutan
files_to_run = [
    "truncate.py",
    "user.py",
    "puskesmas.py",
    "posyandu.py",
    "staffpuskesmas.py",
    "staffposyandu.py",
    "kk.py",
    "nik.py",
    "anak.py",
    "nikchild.py",
    "detail.py",
    "allmed.py",
    "questincome.py"
]


# Fungsi untuk menjalankan file Python
def run_file(file_name):
    try:
        subprocess.run(["python3", file_name], check=True)
        print(f"Sukses menjalankan {file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan {file_name}: {e}")


# Jalankan setiap file dalam urutan
for file in files_to_run:
    run_file(file)

print("Semua file telah dijalankan.")
