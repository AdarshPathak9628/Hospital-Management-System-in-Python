import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='hospital_db'
        )
        if mydb.is_connected():
            print("Connected to MySQL database")
        return mydb
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(mydb):
    if mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")
    
# Function to ensure at least one hospital exists in the table
def ensure_default_hospital(hospital_id, name, address, phone, email):
    mydb = create_connection()
    if mydb is None:
        return

    cursor = mydb.cursor()
    try:
        # Insert hospital credentials into hospital table
        hospital_insert_query = """
        INSERT INTO hospital (hospital_id, name, address, phone, email)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(hospital_insert_query, (hospital_id, name, address, phone, email))
        mydb.commit()
        print("Default hospital created.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_connection(mydb)

# Function to get a valid hospital ID from the user
def get_hospital_id(cur):
    cur.execute("SELECT hospital_id, name FROM hospital")
    hospitals = cur.fetchall()
    if not hospitals:
        print("No hospitals found. Please add a hospital first.")
        return None
    print("Available Hospitals:")
    for hospital in hospitals:
        print(f"ID: {hospital[0]}, Name: {hospital[1]}")
    return int(input("Enter the hospital ID: "))

def get_hospital():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM hospital")
    hospitals = cursor.fetchall()
    if not hospitals:
        print("No hospitals found. Please add a hospital first.")
        return None
    print("Available Hospitals:")
    for hospital in hospitals:
        
        print(f"ID:{hospital[0]} , Name:{hospital[1]} , address:{hospital[2]} , phone:{hospital[3]} , email:{hospital[4]}")
    cursor.close() 
    close_connection(connection)

# User Registration (Patients and Doctors)
def signup_user(username, password, user_type):
    mydb = create_connection()
    if mydb is None:
        return
    
    cur = mydb.cursor()
    # Get a valid hospital ID
    hospital_id = get_hospital_id(cur)

    # Insert user credentials into users table
    user_insert_query = """
    INSERT INTO users (username, password, user_type, hospital_id)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(user_insert_query, (username, password, user_type, hospital_id))
    mydb.commit()
    
    print("your username,password are created sussefully")
    # Get the user_id of the newly created user
    user_id = cur.lastrowid

    if user_type == 'patient':
        print("fill patients details")
        # Insert patient details
        patient_insert_query = """
        INSERT INTO patients (user_id, hospital_id, name, address, phone, date_of_birth, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        email = input("Enter your email: ")
        cur.execute(patient_insert_query, (user_id, hospital_id, name, address, phone, date_of_birth, email))
    
    elif user_type == 'doctor':
        print("Fill doctor details :")
        # Insert doctor details
        doctor_insert_query = """
        INSERT INTO doctors (user_id, hospital_id, name, specialization, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        specialization = input("Enter your specialization: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        cur.execute(doctor_insert_query, (user_id, hospital_id, name, specialization, phone, email))

    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Signup successful!")

# Fill Personal Details for user_type
def Fill_details(user_type,user_id):
    mydb = create_connection()
    if mydb is None:
        return
    
    cur = mydb.cursor()
    # Get a valid hospital ID
    hospital_id = get_hospital_id(cur)
    
    if user_type == 'patient':
        print("fill patients details")
        # Insert patient details
        patient_insert_query = """
        INSERT INTO patients (user_id, hospital_id, name, address, phone, date_of_birth, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        email = input("Enter your email: ")
        cur.execute(patient_insert_query, (user_id, hospital_id, name, address, phone, date_of_birth, email))
    
    elif user_type == 'doctor':
        print("Fill doctor details :")
        # Insert doctor details
        doctor_insert_query = """
        INSERT INTO doctors (user_id, hospital_id, name, specialization, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        D="Dr."
        n= input("Enter your name: ")
        name = D + n
        specialization = input("Enter your specialization: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        cur.execute(doctor_insert_query, (user_id, hospital_id, name, specialization, phone, email))

    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Fill Your Details successful!")

# Login and Authentication
def login_user(username, password):
    mydb = create_connection()
    if mydb is None:
        return None

    cur = mydb.cursor()

    login_query = """
    SELECT user_id, user_type FROM users
    WHERE username = %s AND password = %s
    """
    cur.execute(login_query, (username, password))
    user = cur.fetchone()
    
    cur.close()
    close_connection(mydb)

    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None

def display_pending_token():
    mydb = create_connection()
    cur = mydb.cursor()

    token_display_query = """
    select patient_id,token_id,status from tokens where status = 'pending'
    """
    cur.execute(token_display_query)
    disp=cur.fetchall()
    for i in disp:
        patient_id,token_id,status=i
        print(f"Patient_id: {patient_id}")
        print(f"Token_id: {token_id}")
        print(f"Status: {status}")
        print("-" * 30)
        break
    else:
        print("No panding status of patient.")
    mydb.commit()
    cur.close()

def display_token(patient_id):
    mydb = create_connection()
    if mydb is None:
        return None
    cur = mydb.cursor()
    token_display_query = """
    select * from tokens
    """
    cur.execute(token_display_query)
    disp=cur.fetchall()
    for i in disp:
        patient_id,token_id,status=i
        print(f"Patient_id: {patient_id}")
        print(f"Token_id: {token_id}")
        print(f"Status: {status}")
        print("-" * 30)
        break
    else:
        print("No panding status of patient.")
    mydb.commit()
    cur.close()

# Token Management
def issue_token(patient_id, doctor_id):
    mydb = create_connection()
    cur = mydb.cursor()

    token_insert_query = """
    INSERT INTO tokens (patient_id, doctor_id, hospital_id, issue_date)
    VALUES (%s, %s, (SELECT hospital_id FROM patients WHERE patient_id = %s), NOW())
    """
    cur.execute(token_insert_query, (patient_id, doctor_id, patient_id))
    mydb.commit()

    cur.close()
    close_connection(mydb)
    print("Token issued successfully!")

def update_token_status(token_id, status):
    mydb = create_connection()
    cur = mydb.cursor()

    token_update_query = """
    UPDATE tokens SET status = %s, visit_time = NOW() WHERE token_id = %s
    """
    cur.execute(token_update_query, (status, token_id))
    mydb.commit()

    cur.close()
    close_connection(mydb)
    print("Token status updated successfully!")

# Appointment Booking
def book_appointment(patient_id, doctor_id, appointment_date, hospital_id):
    mydb = create_connection()
    cur = mydb.cursor()

    appointment_insert_query = """
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, hospital_id)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(appointment_insert_query, (patient_id, doctor_id, appointment_date, hospital_id))
    mydb.commit()

    issue_token(patient_id, doctor_id)  # Issue a token for the appointment

    cur.close()
    close_connection(mydb)
    print("Appointment booked successfully!")

# Medical Records Management
def add_medical_record(patient_id, doctor_id, diagnosis, treatment,hospital_id):
    mydb = create_connection()
    cur = mydb.cursor()

    medical_record_insert_query = """
    INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment, record_date, hospital_id)
    VALUES (%s, %s, %s, %s, CURDATE(), %s)
    """
    cur.execute(medical_record_insert_query, (patient_id, doctor_id, diagnosis, treatment,hospital_id))
    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Medical record added successfully!")

# Billing and Payments by check by doctor
def generate_bill(patient_id, amount, hospital_id):
    mydb = create_connection()
    cur = mydb.cursor()

    billing_insert_query = """
    INSERT INTO billing (patient_id, amount, hospital_id, payment_status, billing_date)
    VALUES (%s, %s, %s, 'unpaid', NOW())
    """
    cur.execute(billing_insert_query, (patient_id, amount, hospital_id))
    mydb.commit()
    cur.close()
    close_connection(mydb)
    print("Bill generated successfully!")

# Function to display unpaid bills and pay a bill
def pay_bill(patient_id, hospital_id):
    mydb = create_connection()
    cur = mydb.cursor()
    
    # Check for unpaid bills
    select_query = "SELECT bill_id, amount FROM billing WHERE patient_id = %s AND hospital_id = %s AND payment_status = 'unpaid'"
    cur.execute(select_query, (patient_id, hospital_id))
    unpaid_bills = cur.fetchall()

    if unpaid_bills:
        print("Unpaid Bills:")
        for bill in unpaid_bills:
            print(f"Bill ID: {bill[0]}, Amount: {bill[1]}")

        bill_id = int(input("Enter the Bill ID you want to pay: "))
        amount = float(input("Enter the amount to pay: "))
        update_query = "UPDATE billing SET amount = %s, payment_status = 'paid', billing_date = NOW() WHERE bill_id = %s"
        cur.execute(update_query, (amount, bill_id))
        mydb.commit()
        print("Bill paid successfully!")
    else:
        print("No unpaid bills found your bills are paided.")
    
    cur.close()
    close_connection(mydb)

# Doctors Display
def display_doctor_list(filter_type=None, filter_value=None):
    mydb = create_connection()
    cur = mydb.cursor()

    base_query = """
    SELECT doctor_id, name, specialization, phone, email
    FROM doctors
    """
    if filter_type == 'name':
        query = base_query + " WHERE name LIKE %s"
        params = ('%' + filter_value + '%',)
    else:
        query = base_query
        params = ()

    cur.execute(query, params)
    doctors = cur.fetchall()

    if doctors:
        print("Doctor List:")
        for doctor in doctors:
            doctor_id, name, specialization, phone, email = doctor
            print(f"Doctor ID: {doctor_id}")
            print(f"Name: {name}")
            print(f"Specialization: {specialization}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print("-" * 30)
    else:
        print("No doctors found matching the criteria.")

    cur.close()
    close_connection(mydb)

#display doctor profile
def doctor_profile(doctor_id):
    try:
        # Create a database connection
        connection = create_connection()
        cursor = connection.cursor()

        # Define the query to fetch doctor details
        base_query = """
        SELECT doctor_id,user_id,hospital_id, name, specialization, phone, email
        FROM doctors
        WHERE doctor_id = %s
        """
        # Execute the query
        cursor.execute(base_query, (doctor_id,))
        # Fetch the result
        doc = cursor.fetchone()

        # Check if a record was found
        if doc:
            print("\nDoctor Profile")
            print(f"ID: {doc[0]}")
            print(f"Use ID: {doc[1]}")
            print(f"Hostipal ID: {doc[2]}")
            print(f"Name: {doc[3]}")
            print(f"Specialization: {doc[4]}")
            print(f"Phone: {doc[5]}")
            print(f"Email: {doc[6]}")
        else:
            print("No doctor found with the given ID.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Ensure resources are released
        if connection:
            cursor.close()
            connection.close()

# Function to display how many specialization in hospital
def search_specialization():
    mydb = create_connection()
    cur = mydb.cursor()

    base_query = """
    SELECT DISTINCT specialization FROM doctors
    """
    try:
        cur.execute(base_query)
        result = cur.fetchall()
        
        print("Specializations:")
        ad=1
        global dict_specialization
        dict_specialization={}
        for ro in result:
            dict_specialization.setdefault(ad,ro[0])
            print(ad,"-",ro[0])
            ad=ad+1
    except Exception as e:
        print("Error fetching specializations: ", e)
    finally:
        cur.close()
        close_connection(mydb)

# Function to display doctors by specialization
def display_doctor_specialization(choice):
    try:
        mydb = create_connection()  # Establish a connection to the database
        cur = mydb.cursor()  # Create a cursor object

        # Ensure the specialization dictionary is accessible globally
        global dict_specialization

        # Retrieve the chosen specialization based on user input
        ch = dict_specialization.get(choice, None)
        if not ch:
            print("Invalid choice for specialization.")
            return

        # Prepare the query to fetch doctors based on specialization
        base_query = """
        SELECT doctor_id, name, specialization, phone, email
        FROM doctors
        WHERE specialization = %s
        """
        
        # Execute the query with the chosen specialization
        cur.execute(base_query, (ch,))
        doctors = cur.fetchall()

        # Check if any doctors are returned and print their details
        if doctors:
            print("Doctor List:")
            for doctor in doctors:
                doctor_id, name, specialization, phone, email = doctor
                print(f"Doctor ID: {doctor_id}")
                print(f"Name: {name}")
                print(f"Specialization: {specialization}")
                print(f"Phone: {phone}")
                print(f"Email: {email}")
                print("-" * 30)
        else:
            print("No doctors found matching the criteria.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the cursor and connection are closed properly
        cur.close()
        close_connection(mydb)

# View All Appointments
def view_appointments(doctor_id):
    mydb = create_connection()
    cur = mydb.cursor()

    appointment_query = """
    SELECT a.appointment_id, p.name, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = %s
    """
    cur.execute(appointment_query, (doctor_id,))
    appointments = cur.fetchall()

    if appointments:
        print("\nYour Appointments:")
        for appointment in appointments:
            print(f"Appointment ID: {appointment[0]}")
            print(f"Patient Name: {appointment[1]}")
            print(f"Appointment Date: {appointment[2]}")
            print("-" * 30)
    else:
        print("No appointments found.")

    cur.close()
    close_connection(mydb)

# view patient by id
def view_patient(patient_id):
    connection = create_connection()
    cursor = connection.cursor()

    user_query = """
    SELECT * FROM patients where patient_id=%s
    """
    cursor.execute(user_query,(patient_id,))
    user = cursor.fetchone()

    if user:
        print("\nUser details:")
        print(f"Patient ID: {user[0]}")
        print(f"User ID: {user[1]}")
        print(f"Hospital ID: {user[2]}")
        print(f"Name: {user[3]}")
        print(f"Address: {user[4]}")
        print(f"Phone: {user[5]}")
        print(f"Date of birth: {user[6]}")
        print(f"Email Id: {user[7]}")
        print("-" * 30)
    else:
        print("No users found.")
    cursor.close()
    close_connection(connection)

# View All Users
def view_all_users():
    mydb = create_connection()
    cur = mydb.cursor()

    user_query = """
    SELECT user_id, username, user_type FROM users
    """
    cur.execute(user_query)
    users = cur.fetchall()
    if users:
        print("\nAll Users:")
        for user in users:
            print(f"User ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"User Type: {user[2]}")
            print("-" * 30)
    else:
        print("No users found.")

    cur.close()
    close_connection(mydb)

#  View user details
def view_user_dp(username):
    connection = create_connection()
    cursor = connection.cursor()
    base_query=""" select * from users where username=%s
               """
    cursor.execute(base_query,(username,))
    user=cursor.fetchone()
    if user:
        print("\n your user details:")
        print(f"User ID: {user[0]}")
        print(f"Hospital ID: {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Password: {user[3]}")
        print(f"User Type: {user[4]}")
    else:
        print("not found user")
    cursor.close()
    connection.close()

# View All Appointments
def view_all_appointments():
    mydb = create_connection()
    cur = mydb.cursor()

    appointment_query = """
    SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d ON a.doctor_id = d.doctor_id
    """
    cur.execute(appointment_query)
    appointments = cur.fetchall()

    if appointments:
        print("\nAll Appointments:")
        for appointment in appointments:
            print(f"Appointment ID: {appointment[0]}")
            print(f"Patient Name: {appointment[1]}")
            print(f"Doctor Name: {appointment[2]}")
            print(f"Appointment Date: {appointment[3]}")
            print("-" * 30)
    else:
        print("No appointments found.")

    cur.close()
    close_connection(mydb)

# Display Patient Bill
def display_patient_bill(patient_id):
    mydb = create_connection()
    cur = mydb.cursor()

    billing_query = """
    SELECT bill_id, amount, payment_status, billing_date
    FROM billing
    WHERE patient_id = %s
    """
    cur.execute(billing_query, (patient_id,))
    bills = cur.fetchall()

    if bills:
        print(f"Billing details for patient ID {patient_id}:")
        for bill in bills:
            bill_id, amount, payment_status, billing_date = bill
            print(f"Bill ID: {bill_id}")
            print(f"Amount: {amount:.2f}")
            print(f"Payment Status: {payment_status}")
            print(f"Billing Date: {billing_date}")
            print("-" * 30)
    else:
        print("No billing records found for this patient.")

    cur.close()
    close_connection(mydb)

#admin login code 
def admin_login(username, password):
    # Hardcoded credentials for simplicity; consider using a secure method in a real application
    admin_username = "adminadarsh"
    admin_password = "12345"
    if username == admin_username and password == admin_password:
        user_type = "admin"
        user_id = 1
        return (user_id, user_type)
    else:
        print("Invalid credentials")
        return None

# Reporting and Analytics
def view_patient_history(patient_id):
    mydb = create_connection()
    if mydb is None:
        return
    cur = mydb.cursor()
    history_query = """
    SELECT r.record_id, r.diagnosis, r.treatment, r.record_date, d.name as doctor_name
    FROM medical_records r
    JOIN doctors d ON r.doctor_id = d.doctor_id
    WHERE r.patient_id = %s
    """
    cur.execute(history_query, (patient_id,))
    records = cur.fetchall()
    if records:
        for record in records:
            print(f"Record ID: {record[0]}, Diagnosis: {record[1]}, Treatment: {record[2]}, Date: {record[3]}, Doctor: {record[4]}")
            print("-" * 30)
    else:
        print("No medical records found.")
    cur.close()
    close_connection(mydb)

# Main Menu Options
def main_menu(user):
    user_id, user_type = user
    while True:
        print("\nMain Menu")
        if user_type == 'patient':
            print("1. Book Appointment")
            print("2. Pay Bill")
            print("3. Display Doctor List")
            print("4. Display Token")
            print("5. Fill Your Details")
            print("6. Display User Details")
            print("7. View Your Profile")
            print("8. View Hospital Branch")
            print("9. Logout")
            
            choice = int(input("Enter your choice: "))
            if choice == 1:
                search_specialization()
                choice = int(input("Enter your choice: "))
                display_doctor_specialization(choice)
                doctor_id = int(input("Enter doctor's ID: "))
                appointment_date = input("Enter appointment date (YYYY-MM-DD HH:MM:SS): ")
                hospital_id = int(input("Enter hospital ID: "))
                book_appointment(user_id, doctor_id, appointment_date, hospital_id)
            elif choice == 2:
                patient_id = int(input("Enter the patient ID: "))
                hospital_id = int(input("Enter the hospital ID: "))
                pay_bill(patient_id, hospital_id)
            elif choice == 3:
                while True:
                    print("\nDoctor List Options:")
                    print("1. Display All Doctors")
                    print("2. Display Doctors by Specialization")
                    print("3. Display Doctors by Name")
                    print("4. Exit")
                    choice = input("Enter your choice (1-4): ")
                    if choice == '1':
                        display_doctor_list()
                    elif choice == '2':
                        search_specialization()
                        choice = int(input("Enter number for Doctor's specialization: "))
                        display_doctor_specialization(choice)
                    elif choice == '3':
                        name_filter = input("Enter doctor's name: ")
                        display_doctor_list('name', name_filter)
                    elif choice == '4':
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")
            elif choice == 4:
                patient_id = int(input("Enter patient ID: "))
                display_token(patient_id)
            elif choice == 5:
                user_type = input("Enter user type (patient/doctor/admin): ")
                user_id = input("Enter user ID: ")
                Fill_details(user_type, user_id)    
            elif choice == 6:
                username = input("Enter your username: ")
                view_user_dp(username)
            elif choice == 7:
                try:
                    patient_id = int(input("Enter the patient ID: "))
                    view_patient(patient_id)
                except ValueError:
                    print("Invalid patient ID. Please enter a numeric value.")
            elif choice == 8:
                get_hospital()    
            elif choice == 9:
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

        elif user_type == 'doctor':
            print("1. View Appointments")
            print("2. View User Details")
            print("3. Update Token Status")
            print("4. Fill Your Details")
            print("5. Display Profile")
            print("6. Logout")
            
            choice = int(input("Enter your choice: "))
            if choice == 1:
                dr_id = int(input("Enter your ID: "))
                view_appointments(dr_id)
            elif choice == 2:
                username = input("Enter your username: ")
                view_user_dp(username)
            elif choice == 3:
                display_pending_token()
                token_id = int(input("Enter token ID: "))
                status = input("Enter status (completed/pending): ")
                update_token_status(token_id, status)
            elif choice == 4:
                user_type = input("Enter user type (patient/doctor/admin): ")
                user_id = input("Enter user ID: ")
                Fill_details(user_type, user_id) 
            elif choice == 5:
                doctor_id = int(input("Enter your ID: "))
                doctor_profile(doctor_id) 
            elif choice == 6:
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

        elif user_type == 'admin':
            print("1. View All Users")
            print("2. View All Appointments")
            print("3. Display Patient Bill")
            print("4. Create Hospital Database")
            print("5. Generate Bill")
            print("6. Add Medical Record")
            print("7. View Patient History")
            print("8. Logout")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                view_all_users()
            elif choice == 2:
                view_all_appointments()
            elif choice == 3:
                patient_id = int(input("Enter patient ID: "))
                display_patient_bill(patient_id)
            elif choice == 4:
                hospital_id = int(input("Enter hospital ID: "))
                name = "Jila_hospital"
                address = input("Enter address: ") 
                phone = input("Enter phone number: ")
                email = input("Enter email: ")
                ensure_default_hospital(hospital_id, name, address, phone, email)
            elif choice == 5:
                patient_id = int(input("Enter patient ID: "))
                amount = int(input("Enter the amount: "))
                hospital_id = int(input("Enter hospital ID: "))
                generate_bill(patient_id, amount, hospital_id)
            elif choice == 6:
                patient_id = int(input("Enter patient ID: "))
                doctor_id = int(input("Enter doctor ID: "))
                diagnosis = input("Enter diagnosis: ")
                treatment = input("Enter treatment: ")
                hospital_id = int(input("Enter hospital ID: "))
                add_medical_record(patient_id, doctor_id, diagnosis, treatment, hospital_id)
            elif choice == 7:
                patient_id = int(input("Enter patient ID: "))
                view_patient_history(patient_id)
            elif choice == 8:
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")



if __name__ == "__main__":
    print("Welcome to the Hospital Management System!")
    while True:
        print("1. Sign Up")
        print("2. Log In")
        print("3. Admin Login")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = input("Create username: ")
            password = input("Create password: ")
            user_type = input("Enter user type (patient/doctor): ").lower()
            signup_user(username, password, user_type)
        elif choice == 2:
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login_user(username, password)
            if user:
                main_menu(user)
        elif choice == 3:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            user = admin_login(username, password)
            if user:
                main_menu(user)
        elif choice == 4:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

