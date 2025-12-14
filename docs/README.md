# Cyber Security Incident Management System

**Student Name:** ARIA KARIMPOUR  
**Student ID:** M01084412  
**Course:** CST1510 - CW2  
**GitHub Repository:** [AriaAi-star/CW2-CST1510-M01084412](https://github.com/AriaAi-star/CW2-CST1510-M01084412)

---

## 📋 Project Overview

A comprehensive web-based Cyber Security Incident Management System built with Streamlit. This application provides secure authentication, incident tracking, advanced analytics, and AI-powered assistance for managing cybersecurity incidents.

---

## ✨ Key Features

### 🔐 Authentication & Security
- Secure user registration and login system
- Password hashing using bcrypt (cost factor: 12)
- Session management with Streamlit session state
- Username validation (minimum 3 characters, alphanumeric + underscore)
- Password validation (8+ characters, uppercase, lowercase, digit, special character)

### 📊 Dashboard
- Real-time incident metrics (Total, Resolved, Pending, In Progress)
- Interactive visualizations (Donut, Bar, Pie charts)
- Status distribution analysis
- Customizable record display (10/25/50/100/All records)
- Responsive gradient UI design

### 📈 Analytics
- Timeline chart showing incident trends over time
- Severity distribution analysis
- Category-based incident breakdown
- Interactive heatmap matrix
- Comprehensive data insights

### ⚙️ Settings
- Add new incidents with validation
- Delete existing incidents
- Real-time database updates
- Form validation and error handling

### 🤖 AI Chatbot Integration
- OpenAI GPT-4o-mini powered assistant
- Context-aware responses
- Cybersecurity incident guidance
- Integrated in sidebar across all pages

### 👤 Contact Us
- Developer information and photo
- Contact details (Email, LinkedIn, GitHub)
- Professional profile presentation

---

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

---

## 📁 Project Structure

```
CW2-CST1510-M01084412/
├── Home.py                      # Main entry point with authentication
├── Requirements.txt             # Project dependencies
├── .env                         # Environment variables (OpenAI API key)
├── .gitignore                   # Git ignore file
├── app/
│   ├── __init__.py
│   ├── db.py                    # Database connection management
│   ├── incidents.py             # Incident CRUD operations
│   ├── users.py                 # User authentication functions
│   ├── schema.py                # Database schema definitions
│   └── metadata.py              # Metadata management
├── pages/
│   ├── 1_Dashboard.py           # Main dashboard with metrics
│   ├── 2_Analytics.py           # Advanced analytics page
│   ├── 3_Settings.py            # Incident management page
│   └── 4_Contact_Us.py          # Contact information page
├── DATA/
│   ├── cyber_incidents.csv      # Incident dataset
│   ├── user.txt                 # User credentials
│   └── datasets_metadata.csv    # Metadata information
├── docs/
│   └── README.md                # Project documentation
└── photo1.jpeg                  # Developer photo

Database:
└── cyber_security.db            # SQLite database
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- OpenAI API key

### Step 1: Clone the Repository
```bash
git clone https://github.com/AriaAi-star/CW2-CST1510-M01084412.git
cd CW2-CST1510-M01084412
```

### Step 2: Create Virtual Environment
```bash
python3.11 -m venv .venv311
source .venv311/bin/activate  # On macOS/Linux
# .venv311\Scripts\activate    # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r Requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Initialize Database
The database will be automatically created on first run. It includes:
- `cyber_incidents` table with columns: id, incident_id, incident_type, severity, description, status, date_reported, date_resolved

---

## 🏃 Running the Application

### Start the Application
```bash
streamlit run Home.py
```

The application will open in your browser at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://[your-ip]:8501

### Default Login Credentials
Check `DATA/user.txt` for existing users or register a new account.

---

## 💾 Database Schema

### cyber_incidents Table
| Column         | Type    | Description                           |
|----------------|---------|---------------------------------------|
| id             | INTEGER | Primary key (auto-increment)          |
| incident_id    | TEXT    | Unique incident identifier            |
| incident_type  | TEXT    | Type of security incident             |
| severity       | TEXT    | Severity level (Low/Medium/High)      |
| description    | TEXT    | Incident description                  |
| status         | TEXT    | Current status                        |
| date_reported  | TEXT    | Date incident was reported            |
| date_resolved  | TEXT    | Date incident was resolved (nullable) |

---

## 🔒 Security Features

1. **Password Security**
   - Bcrypt hashing with automatic salt generation
   - Cost factor: 12 (2^12 iterations)
   - Secure password verification

2. **Input Validation**
   - Username: 3+ characters, alphanumeric + underscore
   - Password: 8+ characters, mixed case, digit, special character
   - No SQL injection vulnerabilities (parameterized queries)

3. **Session Management**
   - Streamlit session state for user tracking
   - Automatic logout capability
   - Protected page access

4. **API Key Protection**
   - Environment variables for sensitive data
   - .gitignore for .env file
   - No hardcoded credentials

---

## 📊 Features by Page

### 🏠 Home (Authentication)
- User login with credential verification
- New user registration
- Password strength validation
- Session initialization

### 📊 Dashboard
- Metric cards: Total, Resolved, Pending, In Progress incidents
- Interactive charts: Donut, Bar, Pie visualizations
- Status distribution analysis
- Customizable record display

### 📈 Analytics
- Timeline chart: Incident trends over time
- Severity distribution: High, Medium, Low analysis
- Category breakdown: Incident types
- Interactive heatmap matrix

### ⚙️ Settings
- Add new incidents: Form with validation
- Delete incidents: By incident ID
- Real-time database updates
- Success/error notifications

### 📞 Contact Us
- Developer information and photo
- Contact cards: Email, LinkedIn, GitHub
- About Developer section
- Professional presentation

---

## 🤖 AI Chatbot Features

The integrated AI assistant provides:
- Cybersecurity incident guidance
- Best practices recommendations
- Context-aware responses
- Quick access from sidebar
- Powered by OpenAI GPT-4o-mini

---

## 📦 Dependencies

```txt
streamlit
pandas
plotly
bcrypt
openai
python-dotenv
Pillow
```

See `Requirements.txt` for complete list with versions.

---

## 🎨 UI/UX Features

- **Gradient Backgrounds:** Professional visual design
- **Responsive Layouts:** Works on desktop and tablet
- **Interactive Charts:** Hover tooltips and zoom capabilities
- **Custom Styling:** HTML/CSS for enhanced appearance
- **Sidebar Navigation:** Easy page switching
- **Loading States:** User feedback during operations

---

## 📝 Development Notes

### Code Organization
- **Modular Architecture:** Separate modules for database, users, incidents
- **DRY Principle:** Reusable functions across pages
- **Error Handling:** Try-except blocks for robustness
- **Type Hints:** Clear function signatures (where applicable)

### Data Flow
1. User authenticates → Session state updated
2. Dashboard loads incidents → Database query
3. User actions (add/delete) → Database operations
4. Charts update → Real-time data refresh
5. AI queries → OpenAI API calls

---

## 🐛 Known Issues & Solutions

### Issue: Module not found
**Solution:** Ensure virtual environment is activated and dependencies installed

### Issue: Database locked
**Solution:** Close other connections to `cyber_security.db`

### Issue: OpenAI API error
**Solution:** Verify API key in `.env` file and check account credits

---

## 🔮 Future Enhancements

- [ ] Export reports to PDF/Excel
- [ ] Email notifications for new incidents
- [ ] User role management (Admin/Analyst/Viewer)
- [ ] Advanced search and filtering
- [ ] Incident attachment support
- [ ] Audit log for all changes
- [ ] RESTful API endpoints
- [ ] Mobile responsive design improvements

---

## 👨‍💻 Developer

**Aria Karimpour**  
Student ID: M01084412  
Course: CST1510 - Cybersecurity and Data Science  

### Contact
- **Email:** aria.karimpour@example.com
- **GitHub:** [@AriaAi-star](https://github.com/AriaAi-star)
- **LinkedIn:** [Aria Karimpour](https://linkedin.com/in/aria-karimpour)

---

## 📄 License

This project is created for academic purposes as part of CST1510 coursework.

---

## 🙏 Acknowledgments

- Course instructors and teaching assistants
- OpenAI for GPT-4o-mini API
- Streamlit community for documentation
- Plotly for visualization library

---

## 📞 Support

For issues or questions:
1. Check this README for solutions
2. Review code comments in source files
3. Contact the developer via email
4. Open an issue on GitHub repository

---

**Last Updated:** December 14, 2025  
**Version:** 1.0.0
