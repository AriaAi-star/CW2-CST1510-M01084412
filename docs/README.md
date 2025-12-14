# Cyber Security Incident Management System

**Student Name:** ARIA KARIMPOUR  
**Student ID:** M01084412  
**Course:** CST1510 - CW2  
**GitHub Repository:** [AriaAi-star/CW2-CST1510-M01084412](https://github.com/AriaAi-star/CW2-CST1510-M01084412)

**Live Application URL:**
https://cw2-cst1510-m01084412-8xbgalvpzs53vxfxbzb6tw.streamlit.app/

### Start the Application
```bash
streamlit run Home.py
```

The application will open in your browser at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://[your-ip]:8501

## 📋 Project Overview

An extensive web-based Cyber Security Incident Management System developed using Streamlit. This application delivers safe authentication services, incident reporting, detailed analytics, and AI support for dealing with cyber security events.



## ✨ Key Features

### 🔐 Authentication & Security
Secure user registration & login system
- Password Hashing using bcrypt (Cost Factor: 12)
- Managing sessions using Streamlit session state
- Username validation (minimum of 3 characters, alphanumeric +underscore)
- Password Validation (8+ Characters, Uppercase Letter, Lowercase Letter, Number, Special Character)

####  Dashboard
- Real-time incident metrics: Total, Resolved, Pending, In Progress
- Interactive Visualizations (Donut, Bar, Pie charts)
- Status distribution analysis
- Record viewing settings (10/25/50/100
- Responsive Gradient UI Design


### Analytics
- Timeline graph of incident trends by time periods
- Analysis of severity distribution
- Categorized incident analysis
- Interactive heatmap matrix

### ⚙️ Settings
- Add new incidents with validation
- Remove existing incidents
- Real-time database updates
- Form Validation & Error Processing
### AI Chatbot Integration

OpenAI GPT-4o-mini powered assistant

- Context-aware responses
Text
- Guidance on cybersecurity incidents
- Integrated in the sidebar on all pages

### 👤 Contact Us

- Developer information & photo

- Contact information (Email, LinkedIn, GitHub)
- Professional profile presentation


## 🛠️ Technology Stack

### Frontend
- **Streamlit** - Web application framework
- **Plotly Express** - Interactive visualizations
- **HTML/CSS** - Custom styling with gradients

### Backend
- **Python 3.11** - Core programming language
- **SQLite 3** - Database management
- **bcrypt** - Password hashing
- **pandas** - Data processing

### AI Integration
- **OpenAI API** - GPT-4o-mini model
- **python-dotenv** - Environment variable management

### Additional Libraries
- **Pillow (PIL)** - Image processing
- **datetime** - Timestamp handling

## ???? Project Structure

###

```
-
CW2
├── Home.py                     # Main entry point with authentication
├── Requirements.txt         # Dependencias do projeto
└── .env                         # Environment variables (OpenAI API key)
├── .gitignore                      # git ignore file
|--- app/
│   └── __init__.py
│      ├-- db.py                              #    #    Database    connection    management
        │
├── incidents.py              # Incident CRUD operations
└── users.py                 # Functions for user authentication purposes.
├── schema.py                  # database schema definitions
└── metadata.py                # Metadata management
├── pages
├── 1_Dashboard.py           # Main dashboard with metrics
|--- 2_Analytics.py           # Page with advanced analytics information
├── 3_Settings.py              # Page for managing incidents
│   └── 4_Contact_Us.py          # Contact information page
├── DATA/
├── cyber_incidents.csv       # Incident data set
└── ├── user.txt                 # User credentials
├── datasets_metadata.csv      # Metadata information
└── docs
└── README.md                   # Documentation of the project

└── photo1.jpeg                  # Developer photo
DATABASE:

└── cyber_security.db            # SQLite database

```
d

---
## ???? Installation & Setup
# Prerequisites

- Python 3.11 or later versions
- pip (Python Package Manager)
- OpenAI API key
### Étape 1: Cloner le Répertoire

bash
git clone https://github.com
cd CW2-C
```python
### Step 2: Virtual Environment Creation

bash
python3.11 -m venv
source .venv311/bin/activate  # macOS/Linux

.venv311\Scripts\activate     # On Windows
```
c
### STEP 3: INSTALL DEPENDENCIES
```
\

pip install -r Requirements.txt
```
<span

### Step 4: Configuring Environment Variables

Now that

Inside the root directory, add a `.env` file:



bash

OPENAI

```python

### Step 5: Initialize Database

Now that
The database automatically gets created upon running for the first time. It contains:
- Table `cyber_incidents` with the following columns: id, incident_id, incident_type, severity, description, status
---
## ???? Running the Application

Now that
#### Default login credentials
Look for existing users in `DATA/user.txt`, or register for a new one.
---
## ???? Database Schema
Database
### Table: cyber_incidents

| Column         | Type    | Description                           |
-|---------------|---------|---------------------------------------|
-|---------------|---------|---------------------------------------|

|----------------

| id              | INTEGER | Primary key (auto-increment)          |
| incident_id    | TEXT    | Unique incident identifier          |
| incident_type  | TEXT    | Type of security incident           |

| severity     | TEXT    | Severity level (Low/Medium/High)      |
| description    | TEXT    | Incident description                  |
| status         | TEXT    | Current status                        |

| date_reported | TEXT    | Date incident was reported            |
| date_resolved  | TEXT    | Date incident was resolved (nullable) |
---

## ????.Security Features

Security is
1. **Password Security
- Bcrypt hashing with auto-salt generation

- Cost factor: 12 (2^12 iterations)

- Verify password security

2. Input Validation
Username: 3+ characters, alphanumeric + underscore
- Password: 8+ characters, mixed case letters, number, special character
- No SQL injection vulnerabilities (parameterized queries)

3. **Session Management
- Streamlit session state for user tracking
- Automatic logout functionality
- Securing page access

4. API Key Protection
- Environment Variables for Sensitive Data
- .gitignore for .env file
- No hard-coded credentials

---
## ???? Features by Page
### ???? Home (Authentication)
- User login with credential verification

- New user registration
- Password strength validation
- session initialization
### ???? Dashboard

- Metric cards: Total, Resolved, Pending, In Progress incidents

- Interactive charts: Donut, Bar, Pie charts

- Status distribution analysis
- Customize record view
### ???? Analytics
- Timeline graph: Trends of incidents through time
- Distribution of severity: Analysis of High, Medium, and Low severity

- Category Breakdown: Types of Incidents

- Interactive heatmap matrix

### ⚙️ Settings
- Add new incidents: Form with validation
- Erase Incidents: By incident ID
- Real-time database updates
- Success/error notifications
### ???? Contact Us
- Dev information & image
- Business cards: E-mail, LinkedIn, GitHub

Prior

- About Developer page

- Professional presentation

---

## ???? Key AI Chatbot Features
• The online AI assistant offers:
- Cybersecurity incident advice
- Best practices recommendations
- Context-based answers

- Quick access via sidebar

- Powered by OpenAI GPT-4o

---
## ???? Dependencies
```
.txt
Streamlit

pandas
plotly
bcrypt
openai
python-dot

Pillow

+--------------------------------

See `Requirements.txt` for the full list with versions.

-

## UI/UX Features ????

- **Gradient Backgrounds:** Professional Visual Design

- **Responsive Layouts:** Supports desktop and tablet devices

- **Interactive Charts:** Hover tool-tips & Zooming support
- **Custom Styling:** HTML/CSS for better appearance
- **Sidebar Navigation:** Easy page switching
- **Loading States:** Feedback for users during the course of operations
---
## ???? Development Notes
# Code Organization
edu:

+ **Modular Architecture:** Having separate modules for database, users, and incidents.

- **DRY Principle:** Reusable Functions Across Pages

- **Error Handling:** Using try except statements
- **Type Hints:** Function signatures where relevant

#### Data Flow
 Data flow
1. User authenticates → Session state updated
2. Dashboard retrieves incident data → Database query

3. Actions by user (add/delete) → DB operations

4. Charts update → Real-time data refresh

5. AI queries => OpenAI API calls

---

## ???? Known Issues & Solutions

### Problem: Module not found
**Solution:** Virtual Environment should be active, dependencies must be installed.
### Problem: Database locked

**Solution:** Close other connections to `cyber_security.db

### Problem: OpenAI API error

**Solution:** Validate API key in .env file, then check account credits
---
## ???? Future Enhancements
Next
- [ ] Export reports to PDF/Excel

- [ ] Email Notifications for New Incidents

- [ ] User role management (Admin/Analyst/Viewer)
- [ ] Advanced search functionality and filtering - [ ] Incident attachment support - [ ] Audit log of all changes - [ ] RESTful API endpoints - [ ] Mobile Responsive Design Optimizations --- ## ???? Desenv Aria Karimp Code: M01084412 Course: CST 1510 - Cybersecurity & Data Science #### Contact - **Email:** <aria - **GitHub:** [@A - **LinkedIn:** [Aria Kar --- ## ???? License This project is developed for academic purposes as a course requirement for CST1510. ___ ## ???? Acknowled - Course instructors & Teaching Assistants - OpenAI for GPT-4o-mini - Streamlit community for documentation - plotly for data visualization library --- ## ???? Support For issues or questions: 1. Look at this README for answers 2. Examine the comments found in source files 3. Sending an email to the developer 4. Open an issue on GitHub repository --- Last Updated:December 14, 2025 **Version:**