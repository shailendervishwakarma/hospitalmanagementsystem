# hospitalmanagementsystem
A Python and SQLite3 terminal-based Hospital Management System with Role-Based Access Control (Admin, Doctor, Patient, Accountant) designed for Class 12 Computer Science projects.
# 🏥 Vishwakarama Hospital Management System (HMS)

An interactive, terminal-based **Hospital Management System** built using **Python 3** and **SQLite3**. This project features full **Role-Based Access Control (RBAC)** for Administrators, Doctors, Patients, and Accountants (Payroll).

Designed specifically for **Class 12 Computer Science (CBSE / State Boards)** practical exams and Viva.

---

##  Features & User Roles

###  1. Administrator Portal
* Add new Doctors and create their system accounts.
* Add non-clinical staff (Nurses, Compounders).
* View master lists of all Doctors, Staff, Patients, and Scheduled Appointments.

###  2. Doctor Portal
* View appointments assigned to the logged-in doctor.
* Prescribe diagnosis notes and update appointment status to **Completed**.

###  3. Patient Portal
* View available doctors and consultation fees.
* Book new appointments with desired doctors.
* View personal appointment history and doctor diagnosis notes.

###  4. Accountant / HR Portal
* View staff salary rates (Nurses and Compounders).
* Disburse monthly salaries to staff.
* Track historical payroll payment logs.

---

##  Tech Stack

* **Language:** Python 3.x
* **Database:** SQLite3 (Embedded database, no external setup required)
* **Libraries:** `sqlite3`, `datetime`, `sys` (All built-in Python standard libraries)

---

## 🔑 Default Login Credentials

Use these preset credentials when testing or presenting the project:

| Role | Username | Password | Default Actions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full administrative management |
| **Doctor** | `doctor` | `doc123` | Manage assigned patient appointments |
| **Patient** | `patient` | `pat123` | Book appointments & view prescriptions |
| **Accountant** | `accountant` | `acc123` | Manage staff payroll & salary logs |

> **Note:** New patients can also self-register through Option `2` on the main menu.

---
