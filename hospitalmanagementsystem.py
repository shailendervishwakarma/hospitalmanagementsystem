import sqlite3
import datetime
import sys

# -------------------------------------------------------------------
# 1. DATABASE SETUP & SEED DATA
# -------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect("vishwakarama_hospital.db")
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        ref_id INTEGER
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        fee REAL NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        phone TEXT NOT NULL,
        salary REAL NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        app_date TEXT NOT NULL,
        status TEXT DEFAULT 'Scheduled',
        notes TEXT DEFAULT 'Pending'
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_name TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL NOT NULL,
        date TEXT NOT NULL
    )""")

    # Insert default users if database is fresh
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Default Admin & Accountant Logins
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'Admin')")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('accountant', 'acc123', 'Accountant')")
        
        # Default Doctor Login (Username: doctor)
        cursor.execute("INSERT INTO doctors (name, specialization, fee) VALUES ('Dr. Rajesh Sharma', 'Cardiology', 1200)")
        d1_id = cursor.lastrowid
        cursor.execute("INSERT INTO users (username, password, role, ref_id) VALUES ('doctor', 'doc123', 'Doctor', ?)", (d1_id,))

        cursor.execute("INSERT INTO doctors (name, specialization, fee) VALUES ('Dr. Ananya Roy', 'Neurology', 1500)")
        d2_id = cursor.lastrowid
        cursor.execute("INSERT INTO users (username, password, role, ref_id) VALUES ('drananya', 'doc123', 'Doctor', ?)", (d2_id,))

        # Sample Nurses & Compounders
        cursor.execute("INSERT INTO staff (name, role, phone, salary) VALUES ('Kavita Singh', 'Nurse', '9811223344', 35000)")
        cursor.execute("INSERT INTO staff (name, role, phone, salary) VALUES ('Ramesh Kumar', 'Compounder', '9822334455', 25000)")

        # Default Patient Login (Username: patient)
        cursor.execute("INSERT INTO patients (name, age, gender, phone) VALUES ('Aarav Verma', 30, 'Male', '9876543210')")
        p1_id = cursor.lastrowid
        cursor.execute("INSERT INTO users (username, password, role, ref_id) VALUES ('patient', 'pat123', 'Patient', ?)", (p1_id,))

    conn.commit()
    conn.close()


# -------------------------------------------------------------------
# 2. ADMIN MODULE
# -------------------------------------------------------------------
def admin_portal():
    while True:
        print("\n" + "="*45)
        print("    🏥 VISHWAKARAMA HOSPITAL - ADMIN PORTAL")
        print("="*45)
        print("1. Add New Doctor")
        print("2. Add New Nurse / Compounder")
        print("3. View All Doctors")
        print("4. View All Staff (Nurses/Compounders)")
        print("5. View All Registered Patients")
        print("6. View All Appointments")
        print("0. Logout")
        print("-" * 45)

        choice = input("Enter choice (0-6): ").strip()

        conn = sqlite3.connect("vishwakarama_hospital.db")
        cursor = conn.cursor()

        if choice == "1":
            name = input("Enter Doctor Name (e.g., Dr. Vikram Patel): ")
            spec = input("Enter Specialization: ")
            fee = float(input("Enter Consultation Fee (₹): "))
            uname = input("Create Username for Doctor: ")
            pwd = input("Create Password for Doctor: ")

            cursor.execute("INSERT INTO doctors (name, specialization, fee) VALUES (?, ?, ?)", (name, spec, fee))
            doc_id = cursor.lastrowid
            cursor.execute("INSERT INTO users (username, password, role, ref_id) VALUES (?, ?, 'Doctor', ?)", (uname, pwd, doc_id))
            conn.commit()
            print("\n✅ Doctor added successfully!")

        elif choice == "2":
            name = input("Enter Staff Name: ")
            role = input("Enter Role (Nurse/Compounder): ")
            phone = input("Enter Phone Number: ")
            salary = float(input("Enter Salary (₹): "))

            cursor.execute("INSERT INTO staff (name, role, phone, salary) VALUES (?, ?, ?, ?)", (name, role, phone, salary))
            conn.commit()
            print(f"\n✅ {role} added successfully!")

        elif choice == "3":
            cursor.execute("SELECT * FROM doctors")
            data = cursor.fetchall()
            print("\n" + "-"*55)
            print(f"{'ID':<5} | {'Doctor Name':<20} | {'Specialization':<15} | {'Fee (₹)':<8}")
            print("-" * 55)
            for row in data:
                print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15} | ₹{row[3]:<7.2f}")

        elif choice == "4":
            cursor.execute("SELECT * FROM staff")
            data = cursor.fetchall()
            print("\n" + "-"*55)
            print(f"{'ID':<5} | {'Name':<18} | {'Role':<12} | {'Salary (₹)':<10}")
            print("-" * 55)
            for row in data:
                print(f"{row[0]:<5} | {row[1]:<18} | {row[2]:<12} | ₹{row[4]:<9.2f}")

        elif choice == "5":
            cursor.execute("SELECT * FROM patients")
            data = cursor.fetchall()
            print("\n" + "-"*60)
            print(f"{'ID':<5} | {'Patient Name':<18} | {'Age':<5} | {'Gender':<8} | {'Phone':<12}")
            print("-" * 60)
            for row in data:
                print(f"{row[0]:<5} | {row[1]:<18} | {row[2]:<5} | {row[3]:<8} | {row[4]:<12}")

        elif choice == "6":
            cursor.execute("SELECT * FROM appointments")
            data = cursor.fetchall()
            print("\n" + "-"*70)
            print(f"{'ID':<5} | {'Patient':<15} | {'Doctor':<20} | {'Date':<12} | {'Status':<10}")
            print("-" * 70)
            for row in data:
                print(f"{row[0]:<5} | {row[1]:<15} | {row[2]:<20} | {row[3]:<12} | {row[4]:<10}")

        elif choice == "0":
            conn.close()
            break

        conn.close()


# -------------------------------------------------------------------
# 3. DOCTOR MODULE
# -------------------------------------------------------------------
def doctor_portal(user_ref_id):
    conn = sqlite3.connect("vishwakarama_hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM doctors WHERE doctor_id = ?", (user_ref_id,))
    doc_name = cursor.fetchone()[0]
    conn.close()

    while True:
        print("\n" + "="*45)
        print(f"    🏥 DOCTOR PORTAL - {doc_name}")
        print("="*45)
        print("1. View Assigned Appointments")
        print("2. Add Prescription / Medical Notes")
        print("0. Logout")
        print("-" * 45)

        choice = input("Enter choice (0-2): ").strip()

        conn = sqlite3.connect("vishwakarama_hospital.db")
        cursor = conn.cursor()

        if choice == "1":
            cursor.execute("SELECT * FROM appointments WHERE doctor_name = ?", (doc_name,))
            data = cursor.fetchall()
            print("\n" + "-"*70)
            print(f"{'App ID':<7} | {'Patient Name':<18} | {'Date':<12} | {'Status':<10} | {'Notes':<15}")
            print("-" * 70)
            for row in data:
                print(f"{row[0]:<7} | {row[1]:<18} | {row[3]:<12} | {row[4]:<10} | {row[5]:<15}")

        elif choice == "2":
            app_id = int(input("Enter Appointment ID to update: "))
            notes = input("Enter Diagnosis / Medical Notes: ")

            cursor.execute("UPDATE appointments SET status = 'Completed', notes = ? WHERE appointment_id = ?", (notes, app_id))
            conn.commit()
            print("\n✅ Prescription updated successfully!")

        elif choice == "0":
            conn.close()
            break

        conn.close()


# -------------------------------------------------------------------
# 4. PATIENT MODULE
# -------------------------------------------------------------------
def patient_portal(user_ref_id):
    conn = sqlite3.connect("vishwakarama_hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM patients WHERE patient_id = ?", (user_ref_id,))
    pat_name = cursor.fetchone()[0]
    conn.close()

    while True:
        print("\n" + "="*45)
        print(f"    🏥 PATIENT PORTAL - {pat_name}")
        print("="*45)
        print("1. View Available Doctors")
        print("2. Book Appointment")
        print("3. View My Appointments & Notes")
        print("0. Logout")
        print("-" * 45)

        choice = input("Enter choice (0-3): ").strip()

        conn = sqlite3.connect("vishwakarama_hospital.db")
        cursor = conn.cursor()

        if choice == "1":
            cursor.execute("SELECT name, specialization, fee FROM doctors")
            data = cursor.fetchall()
            print("\n" + "-"*50)
            print(f"{'Doctor Name':<20} | {'Specialization':<15} | {'Fee (₹)':<8}")
            print("-" * 50)
            for row in data:
                print(f"{row[0]:<20} | {row[1]:<15} | ₹{row[2]:<7.2f}")

        elif choice == "2":
            doc_name = input("Enter Doctor Name to Book: ")
            app_date = input("Enter Date (YYYY-MM-DD): ")

            cursor.execute("INSERT INTO appointments (patient_name, doctor_name, app_date) VALUES (?, ?, ?)", (pat_name, doc_name, app_date))
            conn.commit()
            print(f"\n✅ Appointment booked with {doc_name} for {app_date}!")

        elif choice == "3":
            cursor.execute("SELECT * FROM appointments WHERE patient_name = ?", (pat_name,))
            data = cursor.fetchall()
            print("\n" + "-"*70)
            print(f"{'App ID':<7} | {'Doctor Name':<20} | {'Date':<12} | {'Status':<10} | {'Notes':<15}")
            print("-" * 70)
            for row in data:
                print(f"{row[0]:<7} | {row[2]:<20} | {row[3]:<12} | {row[4]:<10} | {row[5]:<15}")

        elif choice == "0":
            conn.close()
            break

        conn.close()


# -------------------------------------------------------------------
# 5. ACCOUNTANT MODULE (PAYROLL & SALARY)
# -------------------------------------------------------------------
def accountant_portal():
    while True:
        print("\n" + "="*45)
        print("    🏥 ACCOUNTANT / PAYROLL PORTAL")
        print("="*45)
        print("1. View Staff Salaries")
        print("2. Pay Staff Salary")
        print("3. View Salary Payment History")
        print("0. Logout")
        print("-" * 45)

        choice = input("Enter choice (0-3): ").strip()

        conn = sqlite3.connect("vishwakarama_hospital.db")
        cursor = conn.cursor()

        if choice == "1":
            cursor.execute("SELECT name, role, salary FROM staff")
            data = cursor.fetchall()
            print("\n" + "-"*48)
            print(f"{'Staff Name':<18} | {'Role':<12} | {'Salary (₹)':<10}")
            print("-" * 48)
            for row in data:
                print(f"{row[0]:<18} | {row[1]:<12} | ₹{row[2]:<9.2f}")

        elif choice == "2":
            name = input("Enter Staff Name to Pay: ")
            cursor.execute("SELECT role, salary FROM staff WHERE name = ?", (name,))
            res = cursor.fetchone()

            if res:
                role, salary = res
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO payroll (staff_name, role, salary, date) VALUES (?, ?, ?, ?)", (name, role, salary, today))
                conn.commit()
                print(f"\n✅ Salary of ₹{salary} paid to {name} on {today}!")
            else:
                print("\n❌ Staff member not found.")

        elif choice == "3":
            cursor.execute("SELECT * FROM payroll")
            data = cursor.fetchall()
            print("\n" + "-"*60)
            print(f"{'Pay ID':<6} | {'Staff Name':<18} | {'Role':<12} | {'Paid (₹)':<10} | {'Date':<10}")
            print("-" * 60)
            for row in data:
                print(f"{row[0]:<6} | {row[1]:<18} | {row[2]:<12} | ₹{row[3]:<9.2f} | {row[4]:<10}")

        elif choice == "0":
            conn.close()
            break

        conn.close()


# -------------------------------------------------------------------
# 6. GUIDED LOGIN SYSTEM
# -------------------------------------------------------------------
def patient_register():
    print("\n--- PATIENT SELF REGISTRATION ---")
    name = input("Enter Full Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    phone = input("Enter Phone Number: ")
    uname = input("Create Username: ")
    pwd = input("Create Password: ")

    conn = sqlite3.connect("vishwakarama_hospital.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO patients (name, age, gender, phone) VALUES (?, ?, ?, ?)", (name, age, gender, phone))
        pat_id = cursor.lastrowid
        cursor.execute("INSERT INTO users (username, password, role, ref_id) VALUES (?, ?, 'Patient', ?)", (uname, pwd, pat_id))
        conn.commit()
        print(f"\n✅ Account registered! Welcome to Vishwakarama Hospital, {name}. Please log in now.")
    except sqlite3.IntegrityError:
        print("\n❌ Username already exists!")
    finally:
        conn.close()


def guided_login():
    print("\n" + "="*50)
    print("           ❓ WHO ARE YOU LOGGING IN AS?")
    print("="*50)
    print("1. Administrator (Username: admin | Password: admin123)")
    print("2. Doctor        (Username: doctor | Password: doc123)")
    print("3. Patient       (Username: patient | Password: pat123)")
    print("4. Accountant    (Username: accountant | Password: acc123)")
    print("0. Back to Main Menu")
    print("-" * 50)

    role_choice = input("Select who you are (0-4): ").strip()

    if role_choice == "0":
        return

    print("\n" + "─"*35)
    uname = input("Enter Username: ").strip()
    pwd = input("Enter Password: ").strip()

    conn = sqlite3.connect("vishwakarama_hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, ref_id FROM users WHERE username = ? AND password = ?", (uname, pwd))
    user = cursor.fetchone()
    conn.close()

    if user:
        role, ref_id = user
        print(f"\n✅ Login Successful! Welcome [{role}]")
        if role == "Admin":
            admin_portal()
        elif role == "Doctor":
            doctor_portal(ref_id)
        elif role == "Patient":
            patient_portal(ref_id)
        elif role == "Accountant":
            accountant_portal()
    else:
        print("\n❌ Invalid Username or Password!")


def main():
    init_db()

    while True:
        print("\n" + "═"*50)
        print("   🏥 VISHWAKARAMA HOSPITAL MANAGEMENT SYSTEM")
        print("═"*50)
        print("1. Login to Portal")
        print("2. Register as New Patient")
        print("0. Exit Program")
        print("-" * 50)

        choice = input("Select Option (0-2): ").strip()

        if choice == "1":
            guided_login()
        elif choice == "2":
            patient_register()
        elif choice == "0":
            print("\n👋 Thank you for using Vishwakarama Hospital System. Goodbye!")
            sys.exit()


if __name__ == "__main__":
    main()