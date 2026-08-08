import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode

st.set_page_config(page_title="سوق المروة - النظام الإداري المتكامل", layout="wide")

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, barcode TEXT",
        "clients": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT",
        "sales": "id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, quantity_sold INTEGER, price REAL, client_name TEXT, date TEXT",
        "expenses": "id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, category TEXT, date TEXT",
        "debts": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, remaining REAL, notes TEXT",
        "employees": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT, salary REAL, phone TEXT",
        "projects": "id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT, budget REAL"
    }
    for table, schema in tables.items():
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
    conn.commit()
    conn.close()

init_db()

st.title("🛒 سوق المروة للأثاث والديكور - لوحة التحكم الشاملة")
tabs = st.tabs([
    "📊 المؤشرات", "📦 المخزون", "🖨️ QR Code", "👥 العملاء", 
    "📈 الصفقات والمبيعات", "📊 التقارير", "💰 الديون", 
    "💸 المصروفات", "🏗️ المشاريع", "🏅 الموظفين"
])

# 1. المؤشرات
with tabs[0]:
    st.subheader("📊 لوحة المؤشرات والأداء المالي")
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    tot_sales = df_s['price'].sum() if not df_s.empty else 0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0
    tot_debts = df_d['remaining'].sum() if not df_d.empty else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 إجمالي المبيعات", f"{tot_sales:,.1f} ج.م")
    c2.metric("💸 إجمالي المصروفات", f"{tot_exp:,.1f} ج.م")
    c3.metric("📈 صافي الربح التقديري", f"{tot_sales - tot_exp:,.1f} ج.م")
    c4.metric("⚠️ إجمالي الديون الآجلة", f"{tot_debts:,.1f} ج.م")

# 2. المخزون
with tabs[1]:
    st.subheader("📦 إدارة المخزون والمنتجات")
    conn = sqlite3.connect(DB_PATH)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_q = st.text_input("🔍 بحث سريع في المخزون (بالاسم أو الكود):")
    
    if search_q:
        df_p = pd.read_sql(f"SELECT * FROM products_catalog WHERE name LIKE '%{search_q}%' OR barcode LIKE '%{search_q}%'", conn)
    else:
        df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
        
    st.dataframe(df_p, use_container_width=True)
    
    with st.expander("➕ إضافة منتج جديد للمخزون"):
        with st.form("add_prod_full", clear_on_submit=True):
            n = st.text_input("اسم المنتج")
            p = st.number_input("السعر", min_value=0.0)
            q = st.number_input("الكمية المتاحة", min_value=0, step=1)
            b = st.text_input("كود المنتج أو الباركود (مثل: AMIN1995)")
            if st.form_submit_button("حفظ المنتج"):
                conn.execute("INSERT INTO products_catalog (name, price, quantity, barcode) VALUES (?,?,?,?)", (n, p, q, b))
                conn.commit(); st.rerun()
                
    # زر لحذف منتج
    if not df_p.empty:
        with st.expander("🗑️ حذف منتج من المخزون"):
            del_id = st.selectbox("اختر رقم معرف المنتج للحذف (ID):", df_p['id'].tolist())
            if st.button("حذف المنتج المحدد"):
                conn.execute("DELETE FROM products_catalog WHERE id = ?", (del_id,))
                conn.commit(); st.rerun()
    conn.close()

# 3. توليد QR Code
with tabs[2]:
    st.subheader("🖨️ توليد وطباعة QR Code للاستيكرات")
    q_text = st.text_input("أدخل كود المنتج أو البيانات للطباعة:", value="AMIN1995")
    if st.button("إنشاء الاستيكر"):
        if q_text.strip() != "":
            img = qrcode.make(q_text)
            img.save("qrcode_gen.png")
            st.image("qrcode_gen.png", width=250)
            st.success("تم التوليد بنجاح! جاهز للطباعة واللزق على المنتج.")
        else:
            st.warning("الرجاء إدخال الكود أولاً.")

# 4. العملاء
with tabs[3]:
    st.subheader("👥 سجل وإدارة العملاء")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_client_full", clear_on_submit=True):
        c_name = st.text_input("اسم العميل بالكامل")
        c_phone = st.text_input("رقم الهاتف / الموبايل")
        c_addr = st.text_input("العنوان / المنطقة")
        if st.form_submit_button("حفظ بيانات العميل"):
            conn.execute("INSERT INTO clients (name, phone, address) VALUES (?,?,?)", (c_name, c_phone, c_addr))
            conn.commit(); st.rerun()
    df_c = pd.read_sql("SELECT * FROM clients", conn)
    st.dataframe(df_c, use_container_width=True)
    conn.close()

# 5. الصفقات والمبيعات
with tabs[4]:
    st.subheader("📈 تسجيل ومتابعة الصفقات اليومية")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_sale_full", clear_on_submit=True):
        s_prod = st.text_input("اسم المنتج المباع")
        s_client = st.text_input("اسم العميل (اختياري)")
        s_qty = st.number_input("الكمية المباعة", min_value=1, value=1)
        s_price = st.number_input("إجمالي السعر المدفوع", min_value=0.0)
        if st.form_submit_button("تأكيد وتسجيل الصفقة"):
            conn.execute("INSERT INTO sales (product_name, quantity_sold, price, client_name, date) VALUES (?,?,?,?,?)", 
                         (s_prod, s_qty, s_price, s_client, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()
    df_s_all = pd.read_sql("SELECT * FROM sales", conn)
    st.dataframe(df_s_all, use_container_width=True)
    conn.close()

# 6. التقارير
with tabs[5]:
    st.subheader("📊 التقارير والرسوم البيانية التفصيلية")
    conn = sqlite3.connect(DB_PATH)
    df_sales_rep = pd.read_sql("SELECT * FROM sales", conn)
    if not df_sales_rep.empty:
        st.write("🏆 حركة المبيعات وأكثر المنتجات طلباً:")
        st.bar_chart(df_sales_rep.groupby('product_name')['quantity_sold'].sum())
        st.markdown("---")
        st.dataframe(df_sales_rep, use_container_width=True)
    else:
        st.info("لا توجد بيانات كافية لعمل التقارير حالياً.")
    conn.close()

# 7. الديون
with tabs[6]:
    st.subheader("💰 حسابات الديون والآجل للعملاء")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_debt_full", clear_on_submit=True):
        d_client = st.text_input("اسم العميل المدين")
        d_amount = st.number_input("المبلغ المتبقي (آجل)", min_value=0.0)
        d_notes = st.text_input("ملاحظات / تفاصيل الدين")
        if st.form_submit_button("حفظ الدين"):
            conn.execute("INSERT INTO debts (client_name, remaining, notes) VALUES (?,?,?)", (d_client, d_amount, d_notes))
            conn.commit(); st.rerun()
    df_d_all = pd.read_sql("SELECT * FROM debts", conn)
    st.dataframe(df_d_all, use_container_width=True)
    conn.close()

# 8. المصروفات
with tabs[7]:
    st.subheader("💸 إدارة المصروفات والنثريات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_exp_full", clear_on_submit=True):
        ex_reason = st.text_input("بند أو سبب المصروف")
        ex_amount = st.number_input("قيمة المبلغ المنصرف", min_value=0.0)
        ex_cat = st.selectbox("تصنيف المصروف", ["نثريات", "إيجار ورشة/معرض", "نقل وتوصيل", "أدوات وخامات", "أخرى"])
        if st.form_submit_button("تسجيل المصروف"):
            conn.execute("INSERT INTO expenses (reason, amount, category, date) VALUES (?,?,?,?)", 
                         (ex_reason, ex_amount, ex_cat, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()
    df_ex_all = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df_ex_all, use_container_width=True)
    conn.close()

# 9. المشاريع
with tabs[8]:
    st.subheader("🏗️ متابعة مشاريع الديكور والتشطيبات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_proj_full", clear_on_submit=True):
        pr_name = st.text_input("اسم المشروع (مثال: تشطيب شقة المهندس فلان)")
        pr_client = st.text_input("اسم صاحب المشروع")
        pr_status = st.selectbox("حالة العمل", ["تحت المعاينة", "جاري التنفيذ بالورشة", "جاري التركيب بالموقع", "مكتمل وتسليم تام", "مؤجل"])
        pr_budget = st.number_input("قيمة مقايسة المشروع المتفق عليها", min_value=0.0)
        if st.form_submit_button("حفظ المشروع الجديد"):
            conn.execute("INSERT INTO projects (project_name, client_name, status, budget) VALUES (?,?,?,?)", 
                         (pr_name, pr_client, pr_status, pr_budget))
            conn.commit(); st.rerun()
    df_pr_all = pd.read_sql("SELECT * FROM projects", conn)
    st.dataframe(df_pr_all, use_container_width=True)
    conn.close()

# 10. الموظفين
with tabs[9]:
    st.subheader("🏅 شؤون الموظفين وفريق العمل والرواتب")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_emp_full", clear_on_submit=True):
        em_name = st.text_input("اسم الموظف أو الصنايعي")
        em_role = st.text_input("التخصص (فني دهان، نقاش، مشرف، إلخ)")
        em_salary = st.number_input("الراتب المتفق عليه", min_value=0.0)
        em_phone = st.text_input("رقم التواصل")
        if st.form_submit_button("حفظ بيانات الموظف"):
            conn.execute("INSERT INTO employees (name, role, salary, phone) VALUES (?,?,?,?)", (em_name, em_role, em_salary, em_phone))
            conn.commit(); st.rerun()
    df_em_all = pd.read_sql("SELECT * FROM employees", conn)
    st.dataframe(df_em_all, use_container_width=True)
    conn.close()
