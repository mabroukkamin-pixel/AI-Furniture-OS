import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode

st.set_page_config(page_title="سوق المروة - نظام متكامل", layout="wide")

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
tabs = st.tabs(["📊 المؤشرات", "📦 المخزون", "🖨️ توليد QR Code", "👥 العملاء", "📈 الصفقات", "📊 التقارير", "💰 الديون", "💸 المصروفات", "🏗️ المشاريع", "🏅 الموظفين"])

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

# 2. المخزون
with tabs[1]:
    st.subheader("📦 إدارة المخزون")
    conn = sqlite3.connect(DB_PATH)
    barcode_search = st.text_input("🔍 مسح أو البحث بالكود:")
    if barcode_search:
        prod = pd.read_sql(f"SELECT * FROM products_catalog WHERE barcode = '{barcode_search}'", conn)
        if not prod.empty:
            st.success(f"✅ تم العثور على: {prod['name'].iloc[0]}")
            st.write(f'<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&q={prod["name"].iloc[0]}" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            st.dataframe(prod)
        else:
            st.warning("⚠️ المنتج غير موجود.")

    with st.expander("➕ إضافة منتج جديد"):
        with st.form("add_prod", clear_on_submit=True):
            n = st.text_input("اسم المنتج")
            p = st.number_input("السعر", min_value=0.0)
            q = st.number_input("الكمية", min_value=0)
            b = st.text_input("كود المنتج (مثال: AMIN1995)")
            if st.form_submit_button("حفظ"):
                conn.execute("INSERT INTO products_catalog (name, price, quantity, barcode) VALUES (?,?,?,?)", (n, p, q, b))
                conn.commit(); st.rerun()
    
    st.markdown("### قائمة المنتجات الحالية:")
    df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
    st.dataframe(df_p, use_container_width=True)
    conn.close()

# 3. توليد QR Code
with tabs[2]:
    st.subheader("🖨️ توليد وطباعة QR Code للاستيكر")
    q_text = st.text_input("أدخل كود المنتج أو الاسم لتوليد الاستيكر:", value="AMIN1995")
    if st.button("توليد QR Code"):
        if q_text.strip() != "":
            try:
                img = qrcode.make(q_text)
                img.save("qrcode_gen.png")
                st.image("qrcode_gen.png", width=250)
                st.success("تم توليد الـ QR Code بنجاح! جاهز للطباعة واللزق.")
            except Exception as e:
                st.error("حدث خطأ أثناء التوليد.")
        else:
            st.warning("⚠️ الرجاء إدخال نص أو كود أولاً.")

# 4. العملاء
with tabs[3]:
    st.subheader("👥 إدارة العملاء")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_client", clear_on_submit=True):
        c_name = st.text_input("اسم العميل")
        c_phone = st.text_input("رقم الهاتف")
        if st.form_submit_button("حفظ العميل"):
            conn.execute("INSERT INTO clients (name, phone) VALUES (?,?)", (c_name, c_phone))
            conn.commit(); st.rerun()
    st.markdown("### سجل العملاء:")
    df_c = pd.read_sql("SELECT * FROM clients", conn)
    st.dataframe(df_c, use_container_width=True)
    conn.close()

# 5. الصفقات
with tabs[4]:
    st.subheader("📈 تسجيل الصفقات والمبيعات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_sale", clear_on_submit=True):
        prod = st.text_input("اسم المنتج المباع")
        qty = st.number_input("الكمية المباعة", min_value=1)
        price = st.number_input("السعر الإجمالي")
        if st.form_submit_button("إتمام البيع"):
            conn.execute("INSERT INTO sales (product_name, quantity_sold, price, date) VALUES (?,?,?,?)", (prod, qty, price, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()
    st.markdown("### سجل الصفقات السابقة:")
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    st.dataframe(df_s, use_container_width=True)
    conn.close()

# 6. التقارير
with tabs[5]:
    st.subheader("📊 تقارير الأداء والمبيعات")
    conn = sqlite3.connect(DB_PATH)
    df_sales = pd.read_sql("SELECT * FROM sales", conn)
    if not df_sales.empty:
        st.write("🏆 أكثر المنتجات مبيعاً:")
        st.bar_chart(df_sales.groupby('product_name')['quantity_sold'].sum())
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن لتوليد التقارير.")
    conn.close()

# 7. الديون
with tabs[6]:
    st.subheader("💰 إدارة الديون والآجل")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_debt", clear_on_submit=True):
        d_client = st.text_input("اسم العميل المدين")
        d_amount = st.number_input("المبلغ المتبقي", min_value=0.0)
        if st.form_submit_button("حفظ الدين"):
            conn.execute("INSERT INTO debts (client_name, remaining) VALUES (?,?)", (d_client, d_amount))
            conn.commit(); st.rerun()
    st.markdown("### قائمة الديون الحالية:")
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    st.dataframe(df_d, use_container_width=True)
    conn.close()

# 8. المصروفات
with tabs[7]:
    st.subheader("💸 إدارة المصروفات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_exp", clear_on_submit=True):
        reason = st.text_input("سبب المصروف")
        amount = st.number_input("المبلغ", min_value=0.0)
        if st.form_submit_button("تسجيل المصروف"):
            conn.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (reason, amount, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()
    st.markdown("### سجل المصروفات:")
    df_ex = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df_ex, use_container_width=True)
    conn.close()

# 9. المشاريع
with tabs[8]:
    st.subheader("🏗️ متابعة المشاريع والديكور")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_proj", clear_on_submit=True):
        p_name = st.text_input("اسم المشروع أو العميل")
        p_status = st.selectbox("حالة المشروع", ["جاري التنفيذ", "مكتمل", "مؤجل"])
        if st.form_submit_button("حفظ المشروع"):
            conn.execute("INSERT INTO projects (project_name, status) VALUES (?,?)", (p_name, p_status))
            conn.commit(); st.rerun()
    st.markdown("### المشاريع الحالية:")
    df_pr = pd.read_sql("SELECT * FROM projects", conn)
    st.dataframe(df_pr, use_container_width=True)
    conn.close()

# 10. الموظفين
with tabs[9]:
    st.subheader("🏅 إدارة الموظفين والفريق")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_emp", clear_on_submit=True):
        e_name = st.text_input("اسم الموظف")
        e_role = st.text_input("التخصص / الوظيفة")
        e_salary = st.number_input("الراتب", min_value=0.0)
        if st.form_submit_button("حفظ الموظف"):
            conn.execute("INSERT INTO employees (name, role, salary) VALUES (?,?,?)", (e_name, e_role, e_salary))
            conn.commit(); st.rerun()
    st.markdown("### فريق العمل:")
    df_em = pd.read_sql("SELECT * FROM employees", conn)
    st.dataframe(df_em, use_container_width=True)
    conn.close()
