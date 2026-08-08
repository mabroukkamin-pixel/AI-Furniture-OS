import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# إعداد الصفحة
st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# CSS للتنسيق
st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child { position: fixed !important; top: 50px !important; left: 0 !important; right: 0 !important; background-color: #ffffff; z-index: 99999; padding: 10px 20px 0px 20px; border-bottom: 2px solid #f0f2f6; }
    div[data-testid="stTabs"] > div:nth-child(2) { padding-top: 70px !important; }
    </style>
""", unsafe_allow_html=True)

# قاعدة البيانات
DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    # الجداول شاملة عمود الباركود
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, barcode TEXT",
        "clients": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT",
        "sales": "id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, quantity_sold INTEGER, price REAL, date TEXT",
        "expenses": "id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, date TEXT",
        "debts": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, remaining REAL",
        "employees": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT, salary REAL",
        "projects": "id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, status TEXT"
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

# 2. المخزون (بالتنبيهات + الباركود)
with tabs[1]:
    st.subheader("📦 إدارة المخزون")
    conn = sqlite3.connect(DB_PATH)
    
    # تنبيه المخزون المنخفض
    low_stock = pd.read_sql("SELECT name, quantity FROM products_catalog WHERE quantity <= 3", conn)
    if not low_stock.empty:
        st.error("⚠️ تنبيه: المنتجات التالية قاربت على النفاد!")
        st.table(low_stock)
    
    # البحث بالباركود
    st.subheader("🔍 البحث السريع بالباركود")
    barcode_search = st.text_input("امسح الباركود هنا:")
    if barcode_search:
        prod_found = pd.read_sql(f"SELECT * FROM products_catalog WHERE barcode = '{barcode_search}'", conn)
        if not prod_found.empty: st.success("✅ تم العثور على المنتج!"); st.dataframe(prod_found)
        else: st.warning("⚠️ المنتج غير موجود.")

    with st.expander("➕ إضافة منتج جديد"):
        with st.form("add_prod"):
            n = st.text_input("اسم المنتج")
            p = st.number_input("السعر", min_value=0.0)
            q = st.number_input("الكمية", min_value=0)
            b = st.text_input("رقم الباركود")
            if st.form_submit_button("حفظ"):
                conn.execute("INSERT INTO products_catalog (name, price, quantity, barcode) VALUES (?,?,?,?)", (n, p, q, b))
                conn.commit()
                st.rerun()
    
    df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
    st.dataframe(df_p, use_container_width=True)
    conn.close()

# 3. الصفقات
with tabs[3]:
    st.subheader("📈 تسجيل الصفقات")
    with st.form("add_sale"):
        prod = st.text_input("اسم المنتج")
        qty = st.number_input("الكمية المباعة", min_value=1)
        price = st.number_input("السعر الإجمالي")
        if st.form_submit_button("إتمام البيع"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO sales (product_name, quantity_sold, price, date) VALUES (?,?,?,?)", (prod, qty, price, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("تم تسجيل البيع!")

# 4. التقارير
with tabs[4]:
    st.subheader("📊 تقارير الأداء")
    conn = sqlite3.connect(DB_PATH)
    df_sales = pd.read_sql("SELECT * FROM sales", conn)
    if not df_sales.empty:
        st.write("🏆 أكثر المنتجات مبيعاً:")
        st.bar_chart(df_sales.groupby('product_name')['quantity_sold'].sum())
        st.dataframe(df_sales)
    conn.close()

# أقسام فارغة (يمكنك تعبئتها لاحقاً بنفس الطريقة)
with tabs[2]: st.subheader("👥 العملاء")
with tabs[5]: st.subheader("💰 الديون")
with tabs[6]: st.subheader("💸 المصروفات")
with tabs[7]: st.subheader("🏗️ المشاريع")
with tabs[8]: st.subheader("🏅 الموظفين")
