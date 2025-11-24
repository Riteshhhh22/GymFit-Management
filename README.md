GymFit Management WebApp
Overview
GymFit Management is a Flask-based web application designed for secure gym membership management, developed as part of the Secure Web Development Continuous Assessment (CA) at National College of Ireland.
This project demonstrates both the exploitation and mitigation of common web application vulnerabilities as required in the assignment.

Features
Member, trainer, and admin management

Member creation, search, and detail viewing (CRUD)

Secure authentication and session handling

Multiple user roles (admin/member)

Secure SQLite database integration

Vulnerability Demonstration & Fixes
Includes stepwise commits for discovery and patching of:

SQL Injection (login, member search)

Cross-Site Scripting (XSS) (notes field)

Privilege Escalation / IDOR (user profile access)

Each vulnerability has:

Documentation in the technical report

Screenshots of exploits and fixes

GitHub commit history showing remediation

Getting Started
Installation
Clone this repository:

text
git clone https://github.com/Riteshhhh22/GymFit-Management.git
Install requirements:

text
pip install -r requirements.txt
Run the app:

text
python app.py
Usage
Access the login page at localhost:5000

Use sample credentials for admin and member accounts

Manage members, trainers, and user profiles

Security Improvements
All SQL queries use parameterized statements

XSS prevention by escaping user input in templates

Authorization checks to prevent unauthorized data access

Project Structure
text
GymFit-Management/
  ├── app.py
  ├── database.py
  ├── requirements.txt
  ├── templates/
      ├── members.html
      ├── profile.html
      ├── dashboard.html
      └── base.html
Documentation & Report
See the technical report (provided separately) for detailed explanations, screenshots, and references.

Demo
Unlisted YouTube Demo Link

Repository Link

Author
Ritesh Indore, National College of Ireland
