# توضیحات کامل کد پروژه - CW2-CST1510-M01084412

## ساختار پروژه

این یک پروژه Streamlit است که شامل:
- سیستم احراز هویت (Login/Register)
- مدیریت دیتابیس SQLite
- چارت‌های تحلیلی با Plotly
- چت‌بات AI با OpenAI

---

## 1. پوشه app/ - ماژول‌های اصلی

### 📁 app/db.py
**هدف**: اتصال به دیتابیس SQLite

```python
import sqlite3
from pathlib import Path
```
- `sqlite3`: کتابخانه Python برای کار با دیتابیس SQLite
- `Path`: برای کار با مسیر فایل‌ها

```python
DB_PATH = Path(__file__).resolve().parents[1] / 'DATA' / 'inteligent_platform.db'
```
- `__file__`: مسیر فایل فعلی (db.py)
- `.resolve()`: مسیر کامل فایل
- `.parents[1]`: یک پوشه بالاتر (از app/ به root/)
- `/ 'DATA' / ...`: مسیر دیتابیس در پوشه DATA

```python
def connect_database():
    return sqlite3.connect(str(DB_PATH))
```
- تابعی که یک connection به دیتابیس برمی‌گردونه
- `str(DB_PATH)`: تبدیل Path به string

```python
try:
    conn = connect_database()
except Exception:
    conn = None
```
- یک connection سراسری می‌سازه برای استفاده آسان

---

### 📁 app/incidents.py
**هدف**: مدیریت حوادث سایبری

```python
def insert_incident(timestamp, severity, category, status, description):
```
**توضیح خط به خط:**
1. تابع برای اضافه کردن یک حادثه جدید
2. پارامترها:
   - `timestamp`: تاریخ حادثه
   - `severity`: شدت (Critical, High, Medium, Low)
   - `category`: دسته‌بندی (Malware, Phishing, etc.)
   - `status`: وضعیت (Open, Closed, In Progress)
   - `description`: توضیحات

```python
conn = connect_database()
cursor = conn.cursor()
```
- اتصال به دیتابیس
- `cursor`: برای اجرای دستورات SQL

```python
cursor.execute(
    """
    INSERT INTO cyber_incidents
    (timestamp, severity, category, status, description)
    VALUES (?, ?, ?, ?, ?)
    """,
    (timestamp, severity, category, status, description),
)
```
- دستور SQL برای درج داده
- `?` ها جای پارامترها هستن (امنیت در برابر SQL Injection)

```python
conn.commit()
incident_id = cursor.lastrowid
conn.close()
return incident_id
```
- `commit()`: ذخیره تغییرات
- `lastrowid`: ID آخرین رکورد اضافه شده
- `close()`: بستن اتصال
- برگرداندن ID حادثه جدید

```python
def get_all_incidents():
```
**توضیح:**
```python
conn = connect_database()
df = pd.read_sql_query(
    "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
    conn,
)
conn.close()
return df
```
- `pd.read_sql_query`: خوندن نتیجه SQL به DataFrame
- `ORDER BY incident_id DESC`: مرتب‌سازی از جدید به قدیم
- برمی‌گردونه یک DataFrame با همه حوادث

```python
def delete_incident(conn, incident_id):
```
**توضیح:**
```python
cursor = conn.cursor()
cursor.execute(
    "DELETE FROM cyber_incidents WHERE incident_id = ?",
    (incident_id,)
)
conn.commit()
return cursor.rowcount
```
- `DELETE FROM`: پاک کردن رکورد
- `WHERE incident_id = ?`: فقط رکوردی که ID‌ش برابر باشه
- `rowcount`: تعداد ردیف‌های پاک شده (0 یا 1)

---

### 📁 app/metadata.py
**هدف**: مدیریت metadata دیتاست‌ها

```python
def migrate_metadata(conn):
```
**توضیح:**
```python
data_metadata = pd.read_csv('DATA/datasets_metadata.csv')
```
- خواندن فایل CSV

```python
data_metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
```
- `to_sql`: نوشتن DataFrame به جدول SQL
- `if_exists='replace'`: اگه جدول وجود داره، جایگزین کن
- `index=False`: index ستون رو ذخیره نکن

```python
def get_all_datasets_metadata(conn):
    query = "SELECT * FROM datasets_metadata"
    return pd.read_sql_query(query, conn)
```
- گرفتن همه metadata از دیتابیس

---

### 📁 app/users.py
**هدف**: مدیریت کاربران و رمز عبور

```python
import bcrypt
```
- کتابخانه برای hash کردن رمز عبور (امنیت)

```python
def hash_password(plain_password_text):
```
**توضیح خط به خط:**
```python
byted_password = plain_password_text.encode('utf-8')
```
- تبدیل string به bytes (برای bcrypt لازمه)

```python
salt = bcrypt.gensalt()
```
- ساخت یک "نمک" تصادفی (برای امنیت بیشتر)

```python
final_hashed_password = bcrypt.hashpw(byted_password, salt)
```
- hash کردن پسورد با نمک

```python
return final_hashed_password.decode('utf-8')
```
- برگشت به string

```python
def password_verification(plain_password_text, final_hashed_password):
```
**توضیح:**
```python
byted_password = plain_password_text.encode('utf-8')
final_hashed_password = final_hashed_password.encode('utf-8')
return bcrypt.checkpw(byted_password, final_hashed_password)
```
- چک می‌کنه پسورد ساده با hash شده مطابقت داره یا نه
- برمی‌گردونه True/False

```python
def validate_username(username):
```
**قوانین username:**
1. حداقل 3 کاراکتر
2. باید با حرف شروع بشه
3. فقط حروف، اعداد و underscore

```python
if len(username) < 3:
    return False, "Username must be at least 3 characters long."
```
- چک طول

```python
if not username[0].isalpha():
    return False, "Username must start with a letter."
```
- اولین کاراکتر باید حرف باشه

```python
if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
    return False, "Username can only contain letters, digits, and underscores."
```
- regex برای چک کردن فرمت

```python
def validate_password(password):
```
**قوانین password:**
1. حداقل 8 کاراکتر
2. حداقل یک حرف کوچک
3. حداقل یک حرف بزرگ
4. حداقل یک عدد
5. حداقل یک کاراکتر خاص
6. بدون فاصله

```python
if len(password) < 8:
    return False, "Password must be at least 8 characters long."
```
- چک طول

```python
if not re.search(r'[a-z]', password):
    return False, "Password must contain a lowercase letter."
```
- چک حرف کوچک

```python
if not re.search(r'[A-Z]', password):
    return False, "Password must contain an uppercase letter."
```
- چک حرف بزرگ

```python
if not re.search(r'[0-9]', password):
    return False, "Password must contain a digit."
```
- چک عدد

```python
if not re.search(r'[\W_]', password):
    return False, "Password must contain a special character."
```
- چک کاراکتر خاص (!@#$%^ وغیره)

---

### 📁 app/iticket.py
**هدف**: مدیریت تیکت‌های IT

```python
def create_it_tickets_table(conn):
```
**توضیح:**
```python
create_table_sql = """
CREATE TABLE IF NOT EXISTS it_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT UNIQUE NOT NULL,
    priority TEXT CHECK(priority IN ('Critical', 'High', 'Medium', 'Low')),
    status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    ...
)
"""
```
- `PRIMARY KEY AUTOINCREMENT`: ID خودکار
- `UNIQUE NOT NULL`: باید یکتا و پر باشه
- `CHECK(...)`: محدودیت مقادیر مجاز
- `DEFAULT 'Open'`: مقدار پیش‌فرض

---

### 📁 app/schema.py
**هدف**: ایجاد جدول users

```python
def create_users_table(conn):
```
**توضیح:**
```python
create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
```
- جدولی برای ذخیره اطلاعات کاربران
- `TIMESTAMP`: زمان ثبت‌نام خودکار

---

## 2. فایل‌های اصلی Root

### 📄 Home.py
**هدف**: صفحه اصلی با سیستم Login/Register

```python
import streamlit as st
import os
```
- `streamlit`: فریمورک وب
- `os`: کار با فایل‌ها

```python
st.set_page_config(page_title="My App", page_icon="🔐")
```
- تنظیمات صفحه (عنوان و آیکون)

```python
USER_FILE = "DATA/user.txt"
```
- مسیر فایل ذخیره کاربران

```python
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    username, password = line.split(',', 1)
                    users[username] = password
    return users
```
**توضیح خط به خط:**
1. یک dictionary خالی می‌سازه
2. اگه فایل وجود داره
3. فایل رو باز می‌کنه
4. هر خط رو می‌خونه
5. فضای خالی اول و آخر رو پاک می‌کنه
6. اگه کاما داره، split می‌کنه
7. username و password رو جدا می‌کنه
8. به dictionary اضافه می‌کنه
9. dictionary رو برمی‌گردونه

```python
def save_user(username, password):
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{password}\n")
```
- `'a'`: append mode (اضافه کردن به آخر فایل)
- فرمت: `username,password` در هر خط

```python
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
```
- session state: متغیرهایی که بین rerun ها حفظ میشن
- اگه `logged_in` وجود نداره، False بذار

```python
tab1, tab2 = st.tabs(["Login", "Register"])
```
- دو تب برای Login و Register

```python
with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
```
- `text_input`: جعبه متن
- `type="password"`: نمایش به صورت ستاره
- `key`: شناسه یکتا برای هر widget

```python
if st.button("Login"):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login successful!")
        st.rerun()
```
**منطق:**
1. اگه دکمه Login زده شد
2. چک کن username وجود داره
3. چک کن password درسته
4. اگه درسته، logged_in رو True کن
5. username رو ذخیره کن
6. پیام موفقیت نشون بده
7. صفحه رو reload کن

```python
else:
    st.error("Invalid username or password")
```
- اگه اطلاعات اشتباه بود، خطا نشون بده

```python
with tab2:
    new_user = st.text_input("Username", key="reg_user")
    new_pass = st.text_input("Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
```
- سه فیلد: username، password، confirm password

```python
if st.button("Register"):
    if new_user in st.session_state.users:
        st.error("Username already exists")
    elif new_pass != confirm_pass:
        st.error("Passwords don't match")
    elif new_user and new_pass:
        st.session_state.users[new_user] = new_pass
        save_user(new_user, new_pass)
        st.success("Registration successful! Please login.")
```
**منطق ثبت‌نام:**
1. اگه username قبلاً وجود داره → خطا
2. اگه دو پسورد یکی نیستن → خطا
3. اگه همه چی درسته:
   - به dictionary اضافه کن
   - توی فایل ذخیره کن
   - پیام موفقیت

```python
else:
    st.success(f"✅ Welcome, {st.session_state.username}!")
```
- اگه لاگین باشه، خوش‌آمد گو

```python
col1, col2 = st.columns(2)
with col1:
    st.metric("Status", "Logged In")
with col2:
    st.metric("User", st.session_state.username)
```
- دو ستون برای نمایش اطلاعات
- `metric`: نمایش آمار

```python
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
```
- دکمه خروج: logged_in رو False کن و reload

---

## 3. پوشه pages/

### 📄 pages/1_Dashboard.py
**هدف**: صفحه داشبورد با آمار

```python
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.info("Go to Home page to login")
    st.stop()
```
**حفاظت صفحه:**
- اگه لاگین نیستی → پیام هشدار
- `st.stop()`: اجرا رو متوقف کن (بقیه کد اجرا نمیشه)

```python
with st.sidebar:
    st.subheader("🤖 AI Assistant")
    user_msg = st.text_input("Ask me anything:")
    if st.button("Send") and user_msg:
```
- `sidebar`: نوار کناری
- یک chatbot ساده

```python
        with st.spinner("Thinking..."):
            client = OpenAI(api_key="...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_msg}]
            )
            st.success(response.choices[0].message.content)
```
**توضیح AI:**
1. `spinner`: نمایش loading
2. ساخت client با API key
3. ارسال پیام به OpenAI
4. `model`: مدل هوش مصنوعی
5. `messages`: لیست پیام‌ها (فرمت chat)
6. `response.choices[0].message.content`: جواب AI
7. نمایش جواب

```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Users", "150")
with col2:
    st.metric("Sales", "$12,345")
with col3:
    st.metric("Growth", "23%", delta="5%")
```
- سه ستون با آمار
- `delta`: تغییرات (↑ یا ↓)

---

### 📄 pages/2_Analytics.py
**هدف**: صفحه نمودارها

```python
import plotly.express as px
```
- `plotly`: کتابخانه نمودارهای تعاملی

```python
pie_data = pd.DataFrame({
    'Category': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Value': [30, 25, 20, 25]
})
```
- ساخت یک DataFrame با داده‌های نمونه

```python
fig_pie = px.pie(pie_data, values='Value', names='Category', title='Market Share')
st.plotly_chart(fig_pie)
```
**نمودار دایره‌ای:**
- `values`: مقادیر (اندازه هر تکه)
- `names`: نام‌ها (برچسب‌ها)
- `title`: عنوان
- `st.plotly_chart`: نمایش در Streamlit

```python
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [45, 52, 48, 65, 70, 68]
growth = [10, 15, -8, 35, 8, -3]
```
- داده‌های نمونه برای نمودار میله‌ای + خطی

```python
fig = px.bar(x=months, y=revenue, labels={'x': 'Month', 'y': 'Revenue ($K)'})
```
- نمودار میله‌ای درآمد

```python
fig.add_scatter(x=months, y=growth, name='Growth (%)', yaxis='y2', mode='lines+markers')
```
- اضافه کردن یک خط (growth)
- `yaxis='y2'`: محور Y دوم (سمت راست)
- `mode='lines+markers'`: خط + نقطه

```python
fig.update_layout(
    yaxis2=dict(overlaying='y', side='right', title='Growth (%)'),
    showlegend=True
)
```
- تنظیمات layout:
  - محور Y دوم روی محور اول
  - سمت راست
  - نمایش راهنما (legend)

---

## 4. فایل‌های تست

### 📄 main.py
```python
from app.db import connect_database
from app.incidents import get_all_incidents

conn = connect_database()
print("Connected!")

incidents = get_all_incidents()
print(f"\nTotal incidents: {len(incidents)}")
print(incidents.head(3))

conn.close()
```
**توضیح:**
- یک تست ساده
- اتصال به دیتابیس
- گرفتن همه حوادث
- نمایش 3 تا اول
- بستن اتصال

### 📄 test.py
```python
from app.db import connect_database

conn = connect_database()
print("Database connected!")
conn.close()
```
**توضیح:**
- تست خیلی ساده
- فقط چک می‌کنه اتصال کار می‌کنه

### 📄 test_openai.py
```python
from openai import OpenAI

client = OpenAI(api_key="...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "write a haiku about ai"}]
)

print(response.choices[0].message.content)
```
**توضیح:**
- تست OpenAI API
- می‌خواد یک haiku بنویسه
- جواب رو print می‌کنه

---

## خلاصه کلی

### ساختار پروژه:
1. **app/**: ماژول‌های اصلی (دیتابیس، کاربران، حوادث)
2. **Home.py**: صفحه login/register
3. **pages/**: صفحات مختلف Streamlit
4. **DATA/**: دیتابیس و فایل‌های CSV
5. **test files**: تست‌های ساده

### تکنولوژی‌ها:
- **Streamlit**: فریمورک وب Python
- **SQLite**: دیتابیس فایل-محور
- **Pandas**: کار با داده
- **Plotly**: نمودارهای تعاملی
- **OpenAI**: هوش مصنوعی
- **bcrypt**: امنیت رمز عبور

### جریان کار:
1. کاربر وارد Home.py میشه
2. Login/Register می‌کنه
3. اطلاعات در DATA/user.txt ذخیره میشه
4. بعد از login، به صفحات دیگه دسترسی داره
5. هر صفحه یک chatbot AI داره
6. داده‌ها از SQLite خونده میشن
7. نمودارها با Plotly نمایش داده میشن
