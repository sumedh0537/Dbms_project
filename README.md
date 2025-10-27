# Job Portal Web Application (DBMS Project)

A simple **Job Portal System** built using **Flask**, **MySQL**, HTML, CSS, and JavaScript.  
This project demonstrates CRUD operations, user authentication, relational data management, and database integration in a web application.

---

## 🗂️ Database Schema

### 1. `users`
| Field | Type | Key | Description |
|-------|------|-----|-------------|
| id | int | Primary | Unique user ID |
| name | varchar(100) |  | User's full name |
| email | varchar(100) | Unique | Used for login |
| password | varchar(100) |  | Hashed user password |

### 2. `companies`
| Field | Type | Key | Description |
|-------|------|-----|-------------|
| id | int | Primary | Unique company ID |
| name | varchar(255) |  | Company name |
| description | text |  | Company details |
| location | varchar(255) |  | Company location |
| created_at | timestamp |  | Record creation time |

### 3. `applications`
| Field | Type | Key | Description |
|-------|------|-----|-------------|
| id | int | Primary | Application ID |
| user_id | int | Foreign | Linked to `users.id` |
| company_id | int | Foreign | Linked to `companies.id` |
| application_status | enum('pending','accepted','rejected') |  | Application progress |
| created_at | timestamp |  | Application time |

### 4. `skills`
| Field | Type | Key | Description |
|-------|------|-----|-------------|
| id | int | Primary | Skill record ID |
| user_id | int | Foreign | Linked to `users.id` |
| skill | varchar(255) |  | Skill name |

---

## ⚙️ Features

- 🧑‍💼 **User Registration & Login**
- 🏢 **Company Listing**
- 📄 **Apply to Companies**
- 💡 **Skill Management (Add, Update, Delete)**
- 📅 **Application Status Tracking**
- 🗃️ **MySQL Relational Database Integration**

---

## 🧰 Tech Stack

**Frontend:** HTML, CSS, JavaScript  
**Backend:** Flask (Python)  
**Database:** MySQL  
**Other Tools:** MySQL Workbench, XAMPP/Flask Server

---

## 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/sumedh0537/Dbms_project.git
   cd Dbms_project
   ```

2. Install dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```

3. Import the database schema into MySQL:
   ```sql
   CREATE DATABASE job_portal;
   USE job_portal;
   SOURCE database.sql;
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open your browser at:
   ```
   http://localhost:5000
   ```

---

## 🔍 Interview Talking Points

- Flask routing and CRUD operations (`/add`, `/update`, `/delete` routes)
- MySQL joins between `users`, `companies`, and `applications`
- Use of ENUM for status management
- Session-based user authentication
- JavaScript for UI interactivity (e.g., toggle skill updates)

---

## 📸 Preview

(Add screenshots or demo GIFs here if available)

---

## ✨ Author

**Sumedh Jaltare**  
📧 [jaltaresr@gmail.com](mailto:jaltaresr@gmail.com)  
🎓 Modern College of Engineering, Pune  
