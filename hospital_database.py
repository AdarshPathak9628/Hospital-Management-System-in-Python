'''
user table:==
CREATE TABLE users (user_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,user_type ENUM('patient', 'doctor', 'admin') NOT NULL);

patients table:==
CREATE TABLE patients (patient_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,
name VARCHAR(100) NOT NULL,address VARCHAR(255),phone VARCHAR(15),date_of_birth DATE,
email VARCHAR(100),FOREIGN KEY (user_id) REFERENCES users(user_id));

doctors table:==
CREATE TABLE doctors (doctor_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,
name VARCHAR(100) NOT NULL,specialization VARCHAR(100),phone VARCHAR(15),email VARCHAR(100),
FOREIGN KEY (user_id) REFERENCES users(user_id));

appointments table:==
CREATE TABLE appointments (appointment_id INT AUTO_INCREMENT PRIMARY KEY,patient_id INT NOT NULL,
doctor_id INT NOT NULL,appointment_date DATETIME NOT NULL,
status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id));

medical_records table:==
CREATE TABLE medical_records(record_id INT AUTO_INCREMENT PRIMARY KEY,patient_id INT NOT NULL,
doctor_id INT NOT NULL,diagnosis TEXT,treatment TEXT,record_date DATE,
FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id));

billing:==
CREATE TABLE billing (bill_id INT AUTO_INCREMENT PRIMARY KEY,patient_id INT NOT NULL,
amount DECIMAL(10, 2) NOT NULL,payment_status ENUM('paid', 'unpaid') DEFAULT 'unpaid',
billing_date DATETIME NOT NULL,FOREIGN KEY (patient_id) REFERENCES patients(patient_id));

'''