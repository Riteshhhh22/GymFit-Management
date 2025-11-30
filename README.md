GymFit Management WebApp
Overview
GymFit Management is a Flask-based web application for managing gym members, trainers, and basic account details. The system was built as a small security-focused web app that starts from an intentionally vulnerable version and is then hardened step by step. The project shows how everyday features like login, search, notes, and profile pages can be attacked and then secured using practical coding changes.​

Purpose
The main goal of this project is to demonstrate how a typical CRUD-style gym management system can be designed, implemented, and then strengthened against common web vulnerabilities. The application is used to explore insecure patterns (such as string-built SQL and unescaped output) and then replace them with secure alternatives, while keeping the experience simple for gym staff and admins.​

Educational Use Only
This project is for educational and demonstration purposes only. It is not intended for production use and should not be deployed with real customer data.​

Technologies Used
Python 3.x

Flask

SQLite

Jinja2 templating

HTML, CSS, Bootstrap

Functional Features
User authentication:

Login and logout

Session-based access control

Member management:

Add new members

Search existing members

View member details and notes

Trainer/admin support:

View trainers list (if configured)

User profile:

Each user can view their own profile

Admins can view multiple profiles

Security Features
All database queries use parameterised SQL statements.

User input is escaped in templates to prevent script execution.

Authorization checks ensure users cannot access other users’ profiles.

Session handling restricts protected pages to logged-in users only.​

Vulnerabilities Demonstrated
The project originally contained the following insecure behaviours:

SQL Injection in login

The login query was built by concatenating the username and password into the SQL string.

This allowed an attacker to log in without a valid password using payloads like: admin' OR '1'='1.

SQL Injection in member search

The search query directly embedded the search text into the WHERE clause.

Inputs such as ' OR '1'='1 could return the entire members table instead of filtered results.

Cross-Site Scripting (XSS) in member notes

The notes field was rendered as raw HTML using a “safe” flag in the template.

Stored script tags (for example, <script>alert('XSS')</script>) executed in other users’ browsers.

Privilege escalation / IDOR in profile view

The /profile/<user_id> route did not verify that the logged-in user owned the profile or had admin rights.

Changing the ID in the URL exposed other users’ profiles.​

How These Issues Were Fixed
SQL Injection fixes

All login and member search queries now use parameterised SQL statements.

User inputs are passed as parameters instead of being concatenated into the SQL string, so the database treats them as data rather than commands.

XSS fix

The Jinja2 template no longer marks the notes field as “safe”.

Default escaping is used so any script tags are displayed as plain text instead of being executed by the browser.

Privilege escalation / IDOR fix

The profile route checks the current session user before loading profile data.

Only the profile owner or an admin user is allowed to view a given profile; others see an “Unauthorized access” message and are redirected.​

Security Testing
Static review:

The Python code was manually reviewed to identify unsafe SQL usage, unescaped output, and missing access checks.

Manual security testing:

SQL Injection:

Attempted admin' OR '1'='1 and similar payloads in the login and member search forms before and after fixes.

After the fixes, these payloads are treated as plain input and no longer bypass authentication or dump data.

XSS:

Saved <script>alert('XSS')</script> in the notes field and checked behaviour in the members table view.

After the fix, no popup appears and the text is displayed harmlessly.

IDOR / Privilege escalation:

Logged in as a normal user and changed /profile/<id> in the URL to other IDs.

The updated code now blocks access and redirects with an error message.​

Architecture Overview
At a high level, GymFit Management consists of:

Flask application (app.py) handling:

Routes for login, dashboard, members, and profiles

Session management

Authorization checks

SQLite database (e.g., gym.db) storing:

Users

Members

Optional trainers/roles

Jinja2 HTML templates rendering:

Login page

Dashboard

Member list and details

Profile page

Project Structure (simplified)
GymFit-Management/
app.py
database.py
requirements.txt
templates/
base.html
login.html
dashboard.html
members.html
profile.html
static/
(CSS/JS files if used)

Prerequisites
Python 3.10 or later installed

pip available on your PATH

SQLite (bundled with most Python installations)

Installation
Clone the repository:
git clone https://github.com/Riteshhhh22/GymFit-Management.git

Change into the project directory:
cd GymFit-Management

Install dependencies:
pip install -r requirements.txt

Initialise the database if required:

Run database.py or follow any instructions in the report to create and seed gym.db.

Running the Application
Start the Flask app:
python app.py

Open your browser and go to:
http://localhost:5000

Default Credentials (example)
Update these values if your actual seed data is different.

Admin user:

Username: admin

Password: Admin@123

Member/Staff user:
