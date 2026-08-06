import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS dental_ai")
cursor.execute("USE dental_ai")

# Scans table
cursor.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255),
    patient_id VARCHAR(255),
    filename VARCHAR(255),
    filepath VARCHAR(500),
    modality VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Doctors table (for login/signup)
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    license VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50) DEFAULT '',
    clinic VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Credentials table
cursor.execute("""
CREATE TABLE IF NOT EXISTS credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    credential_type VARCHAR(100),
    credential_number VARCHAR(255),
    issue_date VARCHAR(50),
    expiry_date VARCHAR(50),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
)
""")

conn.commit()
cursor.close()
conn.close()
print("All tables created: scans, doctors, credentials")
