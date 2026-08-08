import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import barcode
from barcode.writer import ImageWriter

st.set_page_config(page_title="سوق المروة - نظام متكامل", layout="wide")

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, barcode TEXT",
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
tabs = st.tabs(["📊 المؤشرات", "📦 المخزون", "🖨️ طباعة الباركود", "📈 الصفقات", "📊 التقارير", "💰 الديون", "💸 المصروفات", "🏗️ المشاريع", "🏅 الموظفين"])

# 1. المخزون (بالبحث والباركود)
with tabs[1]:
    st.subheader("📦 إدارة المخزون")
    conn = sqlite3.connect(DB_PATH)
    
    barcode_search = st.text_input("🔍 مسح الباركود:")
    if barcode_search:
        prod = pd.read_sql(f"SELECT * FROM products_catalog WHERE barcode = '{barcode_search}'", conn)
        if not prod.empty:
            st.success(f"✅ تم العثور على: {prod['name'].iloc[0]}")
            st.write(f'<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&q={prod["name"].iloc[0]}" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            st.dataframe(prod)
        else:
            st.warning("⚠️ المنتج غير موجود.")

    with st.expander("➕ إضافة منتج"):
        with st.form("add_prod"):
            n, p, q, b = st.text_input("الاسم"), st.number_input("السعر"), st.number_input("الكمية"), st.text_input("الباركود")
            if st.form_submit_button("حفظ"):
                conn.execute("INSERT INTO products_catalog (name, price, quantity, barcode) VALUES (?,?,?,?)", (n, p, q, b))
                conn.commit(); st.rerun()
    conn.close()

# 2. طباعة الباركود (الاستيكر) - مع الحماية من الأخطاء
with tabs[2]:
    st.subheader("🖨️ توليد وطباعة الباركود")
    b_code = st.text_input("أدخل رقم الباركود للمنتج (أرقام أو حروف إنجليزية):")
    if st.button("توليد الباركود"):
        if b_code.strip() != "":
            try:
                code = barcode.get('code128', b_code, writer=ImageWriter())
                filename = code.save('barcode_gen')
                st.image(f"{filename}.png")
                st.success("تم توليد الاستيكر بنجاح! يمكنك طباعته الآن.")
            except Exception as e:
                st.error(f"خطأ في توليد الباركود: تأكد من إدخال أحرف أو أرقام إنجليزية صحيحة.")
        else:
            st.warning("⚠️ الرجاء إدخال رقم أو كود صحيح أولاً.")

# 3. باقي الأقسام
with tabs[0]: st.subheader("📊 مؤشرات الأداء")
with tabs[3]: st.subheader("📈 الصفقات")
with tabs[4]: st.subheader("📊 التقارير")
with tabs[5]: st.subheader("💰 الديون")
with tabs[6]: st.subheader("💸 المصروفات")
with tabs[7]: st.subheader("🏗️ المشاريع")
with tabs[8]: st.subheader("🏅 الموظفين")
