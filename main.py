import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# ======================================================================
# 💡 خدعة الـ CSS الاحترافية: تثبيت شريط الـ Tabs في أعلى الشاشة (Sticky)
# ======================================================================
st.markdown("""
    <style>
    /* استهداف شريط الـ Tabs الخاص بـ Streamlit لجعله ثابتاً في الأعلى */
    div[data-testid="stTabs"] > div:first-child {
        position: fixed !important; /* تثبيت العنصر */
        top: 50px !important;       /* المسافة من أعلى الشاشة (تحت شريط المتصفح مباشرة) */
        left: 0 !important;
        right: 0 !important;
        background-color: #ffffff;  /* خلفية بيضاء عشان الكلام ميختلطش باللي تحته */
        z-index: 99999;             /* التأكد إنه دايماً فوق كل حاجة في الصفحة */
        padding: 10px 20px 0px 20px;
        border-bottom: 2px solid #f0f2f6; /* خط جمالي خفيف تحت الشريط */
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1); /* ظل خفيف عشان يبان بارز ومميز */
    }

    /* إزاحة المحتوى الرئيسي لتحت شوية عشان الشريط الثابت ميغطيش عليه في البداية */
    div[data-testid="stTabs"] > div:nth-child(2) {
        padding-top: 70px !important; 
    }
    </style>
    """, unsafe_allow_html=True)
# ======================================================================

# 2. إعداد قاعدة البيانات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_100_matrix.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "project_assets")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, barcode TEXT, image_path TEXT",
        "clients": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, interest TEXT, notes TEXT",
        "sales": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT, payment_method TEXT, branch TEXT, status TEXT, cancel_reason TEXT",
        "debts": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, phone TEXT, total_amount REAL, paid_amount REAL, remaining REAL, status TEXT, due_date TEXT",
        "expenses": "id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, date TEXT, category TEXT, payment_method TEXT, receipt_img TEXT",
        "projects": "id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT, total_cost REAL, paid_cost REAL, notes TEXT, before_img TEXT, after_img TEXT, team TEXT, deadline TEXT, contract_file TEXT",
        "employees": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT, hire_date TEXT, role TEXT, salary REAL",
        "employee_attendance": "id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, date TEXT, status TEXT",
        "employee_bonuses": "id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, amount REAL, reason TEXT, date TEXT",
        "employee_notes": "id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, note TEXT, date TEXT",
        "employee_shifts": "id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, shift_type TEXT, date TEXT"
    }
    for table, schema in tables.items():
        c.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
    
    c.execute("PRAGMA table_info(sales)")
    columns = [col[1] for col in c.fetchall()]
    if 'status' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN status TEXT DEFAULT 'مكتملة'")
    if 'cancel_reason' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN cancel_reason TEXT DEFAULT ''")

    conn.commit()
    conn.close()

init_db()

main_categories = [
    "أثاث التخزين (كبتات وخزانات)",
    "أثاث الجلوس (كنب وكراسي)",
    "الطاولات والمكاتب",
    "استاندات وعرض",
    "ديكور وإضاءة",
    "مفروشات ونوم",
    "منوعات ومواسم"
]

# 3. العنوان الرئيسي
st.title("🛒 سوق المروة للأثاث والديكور")
st.write("أهلاً بك يا أمين، نظام الإدارة والتشغيل السريع.")

# 4. شريط الأقسام العلوي الثابت (Tabs)
tabs = st.tabs([
    "📊 المؤشرات",
    "📦 المخزون",
    "👥 العملاء",
    "📈 الصفقات",
    "📊 التقارير",
    "💰 الآجل والديون",
    "💸 المصروفات",
    "🧾 الفواتير",
    "🏗️ المشاريع",
    "🏅 الموظفين"
])

# ----------------- 1. المؤشرات -----------------
with tabs[0]:
    st.subheader("📊 مؤشرات الأداء والأموال العامة")
    conn = sqlite3.connect(DB_PATH)
    try: df_s = pd.read_sql("SELECT * FROM sales", conn)
    except: df_s = pd.DataFrame()
    try: df_e = pd.read_sql("SELECT * FROM expenses", conn)
    except: df_e = pd.DataFrame()
    try: df_d = pd.read_sql("SELECT * FROM debts", conn)
    except: df_d = pd.DataFrame()
    conn.close()

    if not df_s.empty and 'price' in df_s.columns:
        if 'status' in df_s.columns:
            tot_sales = df_s[df_s['status'] != 'ملغاة']['price'].sum() if not df_s[df_s['status'] != 'ملغاة'].empty else 0.0
        else:
            tot_sales = df_s['price'].sum()
    else:
        tot_sales = 0.0

    tot_exp = df_e['amount'].sum() if not df_e.empty and 'amount' in df_e.columns else 0.0
    net_profit = tot_sales - tot_exp
    total_debts = df_d['remaining'].sum() if not df_d.empty and 'remaining' in df_d.columns else 0.0

    c1, c2 = st.columns(2)
    c1.metric("💰 إجمالي المبيعات", f"{tot_sales:,.1f} د.ك")
    c2.metric("💸 إجمالي المصروفات", f"{tot_exp:,.1f} د.ك")
    c3, c4 = st.columns(2)
    c3.metric("📈 صافي العائد والأرباح", f"{net_profit:,.1f} د.ك")
    c4.metric("⚠️ إجمالي الديون المستحقة", f"{total_debts:,.1f} د.ك")

# ----------------- 2. المخزون -----------------
with tabs[1]:
    st.subheader("📦 إدارة المخزون")
    conn = sqlite3.connect(DB_PATH)
    try:
        df_all_prod = pd.read_sql("SELECT id AS 'رقم ID', category AS 'الفئة', name AS 'المنتج', color AS 'اللون', dims AS 'المقاسات', price AS 'السعر', quantity AS 'الكمية', location AS 'الفرع', barcode AS 'الباركود' FROM products_catalog", conn)
    except:
        df_all_prod = pd.DataFrame()
    conn.close()

    if not df_all_prod.empty:
        st.dataframe(df_all_prod, use_container_width=True)
    else:
        st.info("لا توجد منتجات مسجلة بعد.")

# ----------------- 3. العملاء -----------------
with tabs[2]:
    st.subheader("👥 إدارة العملاء")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM clients", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 4. الصفقات -----------------
with tabs[3]:
    st.subheader("📈 تسجيل صفقة بيع جديدة")
    # (كود تسجيل الصفقات كما هو في النسخ السابقة)
    st.write("الرجاء إضافة المنتجات لتسجيل صفقة.")

# ----------------- 5. التقارير -----------------
with tabs[4]:
    st.subheader("📊 تقارير المبيعات")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM sales", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 6. دفتر الآجل -----------------
with tabs[5]:
    st.subheader("💰 دفتر الآجل")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM debts", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 7. المصروفات -----------------
with tabs[6]:
    st.subheader("💸 إدارة المصروفات")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM expenses", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 8. الفواتير -----------------
with tabs[7]:
    st.subheader("🧾 الفواتير")
    st.write("سيتم عرض الفواتير هنا.")

# ----------------- 9. المشاريع -----------------
with tabs[8]:
    st.subheader("🏗️ إدارة المشاريع")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM projects", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 10. الموظفين -----------------
with tabs[9]:
    st.subheader("🏅 الموظفين")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM employees", conn), use_container_width=True)
    except: pass
    conn.close()
