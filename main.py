import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# --- CSS التنسيق ---
st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child { position: fixed !important; top: 50px !important; left: 0 !important; right: 0 !important; background-color: #ffffff; z-index: 99999; padding: 10px 20px 0px 20px; border-bottom: 2px solid #f0f2f6; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stTabs"] > div:nth-child(2) { padding-top: 70px !important; }
    </style>
""", unsafe_allow_html=True)

# --- إعداد المسارات وقاعدة البيانات ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_100_matrix.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "project_assets")
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    # التأكد من وجود كل الجداول (تم دمج كل ما أسسناه سابقاً)
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, image_path TEXT",
        "clients": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, interest TEXT",
        "sales": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT",
        "expenses": "id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, date TEXT, category TEXT",
        "debts": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, remaining REAL",
        "employees": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT, salary REAL",
        "projects": "id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT"
    }
    for table, schema in tables.items():
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
    conn.commit()
    conn.close()

init_db()

st.title("🛒 سوق المروة للأثاث والديكور")
tabs = st.tabs(["📊 المؤشرات", "📦 المخزون", "👥 العملاء", "📈 الصفقات", "📊 التقارير", "💰 الديون", "💸 المصروفات", "🏗️ المشاريع", "🏅 الموظفين"])

# 1. المؤشرات
with tabs[0]:
    st.subheader("📊 مؤشرات الأداء العامة")
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    tot_sales = df_s['price'].sum() if not df_s.empty else 0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 المبيعات", f"{tot_sales:,.1f}")
    c2.metric("💸 المصروفات", f"{tot_exp:,.1f}")
    c3.metric("📈 صافي الربح", f"{tot_sales - tot_exp:,.1f}")

# 2. المخزون (بالإضافة في الأعلى + التنبيهات)
with tabs[1]:
    st.subheader("📦 إدارة المخزون")
    # التنبيه الذكي
    conn = sqlite3.connect(DB_PATH)
    low_stock = pd.read_sql("SELECT name, quantity FROM products_catalog WHERE quantity <= 3", conn)
    if not low_stock.empty:
        st.error("⚠️ تنبيه: المنتجات التالية قاربت على النفاد!")
        st.table(low_stock)
    
    # الإضافة في الأعلى
    with st.expander("➕ إضافة منتج جديد (يظهر في أسفل القائمة)", expanded=False):
        with st.form("add_prod", clear_on_submit=True):
            name = st.text_input("اسم المنتج:")
            price = st.number_input("السعر:", min_value=0.0)
            quantity = st.number_input("الكمية:", min_value=0)
            if st.form_submit_button("حفظ المنتج"):
                conn.execute("INSERT INTO products_catalog (name, price, quantity) VALUES (?,?,?)", (name, price, quantity))
                conn.commit()
                st.rerun()
    conn.close()
    
    st.markdown("### 📋 قائمة المنتجات")
    conn = sqlite3.connect(DB_PATH)
    df_prod = pd.read_sql("SELECT * FROM products_catalog ORDER BY id ASC", conn) # الأقدم أولاً
    st.dataframe(df_prod, use_container_width=True)
    conn.close()

# 3. باقي الأقسام (العملاء، الصفقات، الموظفين، إلخ...)
with tabs[2]: st.subheader("👥 العملاء") # كودك السابق...
with tabs[3]: st.subheader("📈 الصفقات") # كودك السابق...
with tabs[4]: 
    st.subheader("📊 تقارير الأرباح التفصيلية")
    conn = sqlite3.connect(DB_PATH)
    df_sales = pd.read_sql("SELECT * FROM sales", conn)
    if not df_sales.empty:
        st.write("🏆 أكثر المنتجات مبيعاً:")
        st.bar_chart(df_sales.groupby('product_name')['quantity_sold'].sum())
    conn.close()
# ... (يمكنك إكمال باقي الأقسام بنفس الطريقة)
