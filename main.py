import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# --- CSS للتنسيق ---
st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child { position: fixed !important; top: 50px !important; left: 0 !important; right: 0 !important; background-color: #ffffff; z-index: 99999; padding: 10px 20px 0px 20px; border-bottom: 2px solid #f0f2f6; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stTabs"] > div:nth-child(2) { padding-top: 70px !important; }
    </style>
""", unsafe_allow_html=True)

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, barcode TEXT, image_path TEXT",
        "clients": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT, interest TEXT",
        "sales": "id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT",
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

st.title("🛒 سوق المروة للأثاث والديكور")
tabs = st.tabs([
    "📊 المؤشرات", "📦 المخزون", "🖨️ QR Code", "👥 العملاء", 
    "📈 الصفقات", "📊 التقارير", "💰 الديون", 
    "💸 المصروفات", "🏗️ المشاريع", "🏅 الموظفين"
])

# 1. المؤشرات
with tabs[0]:
    st.subheader("📊 مؤشرات الأداء العامة")
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    tot_sales = df_s['price'].sum() if not df_s.empty else 0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0
    tot_debts = df_d['remaining'].sum() if not df_d.empty else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 المبيعات", f"{tot_sales:,.1f}")
    c2.metric("💸 المصروفات", f"{tot_exp:,.1f}")
    c3.metric("📈 صافي الربح", f"{tot_sales - tot_exp:,.1f}")
    c4.metric("⚠️ الديون الآجلة", f"{tot_debts:,.1f}")

# 2. المخزون (مع رفع الصور وزرار التعديل والحذف)
with tabs[1]:
    st.subheader("📦 إدارة المخزون والمنتجات")
    conn = sqlite3.connect(DB_PATH)
    
    # تنبيه المخزون المنخفض
    low_stock = pd.read_sql("SELECT name, quantity FROM products_catalog WHERE quantity <= 3", conn)
    if not low_stock.empty:
        st.error("⚠️ تنبيه: المنتجات التالية قاربت على النفاد!")
        st.table(low_stock)
    
    search_q = st.text_input("🔍 بحث سريع في المخزون (بالاسم أو الباركود):")
    if search_q:
        df_p = pd.read_sql(f"SELECT * FROM products_catalog WHERE name LIKE '%{search_q}%' OR barcode LIKE '%{search_q}%'", conn)
    else:
        df_p = pd.read_sql("SELECT * FROM products_catalog ORDER BY id ASC", conn)
        
    st.dataframe(df_p, use_container_width=True)
    
    # قسم إضافة منتج جديد مع رفع الصورة
    with st.expander("➕ إضافة منتج جديد بالتفاصيل والصورة"):
        with st.form("add_prod_orig", clear_on_submit=True):
            cat = st.text_input("التصنيف (مثال: غرف نوم، طاولات):")
            name = st.text_input("اسم المنتج:")
            color = st.text_input("اللون:")
            dims = st.text_input("المقاسات (مثال: 40×53×120 سم):")
            price = st.number_input("السعر:", min_value=0.0)
            quantity = st.number_input("الكمية:", min_value=0, step=1)
            location = st.text_input("الموقع (المعرض أو المخزن):")
            barcode = st.text_input("كود الباركود / QR (مثال: AMIN1995):")
            
            img_file = st.file_uploader("رفـع صورة المنتج:", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("حفظ المنتج"):
                img_path = ""
                if img_file is not None:
                    os.makedirs("uploads", exist_ok=True)
                    img_path = os.path.join("uploads", img_file.name)
                    with open(img_path, "wb") as f:
                        f.write(img_file.getbuffer())
                        
                conn.execute("""
                    INSERT INTO products_catalog (category, name, color, dims, price, quantity, location, barcode, image_path) 
                    VALUES (?,?,?,?,?,?,?,?,?)
                """, (cat, name, color, dims, price, quantity, location, barcode, img_path))
                conn.commit()
                st.success("تم إضافة المنتج بنجاح!")
                st.rerun()

    # قسم تعديل بيانات منتج موجود
    if not df_p.empty:
        with st.expander("✏️ تعديل بيانات منتج موجود"):
            edit_id = st.selectbox("اختر رقم معرف المنتج (ID) للتعديل:", df_p['id'].tolist(), key="edit_sel")
            prod_row = df_p[df_p['id'] == edit_id].iloc[0]
            
            with st.form("edit_prod_form"):
                e_cat = st.text_input("التصنيف:", value=str(prod_row['category']))
                e_name = st.text_input("اسم المنتج:", value=str(prod_row['name']))
                e_color = st.text_input("اللون:", value=str(prod_row['color']))
                e_dims = st.text_input("المقاسات:", value=str(prod_row['dims']))
                e_price = st.number_input("السعر:", min_value=0.0, value=float(prod_row['price']))
                e_qty = st.number_input("الكمية:", min_value=0, step=1, value=int(prod_row['quantity']))
                e_loc = st.text_input("الموقع:", value=str(prod_row['location']))
                e_bar = st.text_input("الباركود:", value=str(prod_row['barcode']))
                
                if st.form_submit_button("تحديث بيانات المنتج"):
                    conn.execute("""
                        UPDATE products_catalog 
                        SET category=?, name=?, color=?, dims=?, price=?, quantity=?, location=?, barcode=? 
                        WHERE id=?
                    """, (e_cat, e_name, e_color, e_dims, e_price, e_qty, e_loc, e_bar, edit_id))
                    conn.commit()
                    st.success("تم التحديث بنجاح!")
                    st.rerun()

        # قسم حذف منتج
        with st.expander("🗑️ حذف منتج من المخزون"):
            del_id = st.selectbox("اختر رقم معرف المنتج (ID) للحذف:", df_p['id'].tolist(), key="del_sel")
            if st.button("تأكيد الحذف"):
                conn.execute("DELETE FROM products_catalog WHERE id = ?", (del_id,))
                conn.commit()
                st.rerun()
                
    conn.close()

# 3. توليد QR Code
with tabs[2]:
    st.subheader("🖨️ توليد وطباعة QR Code للاستيكر")
    q_text = st.text_input("أدخل الكود أو النص للطباعة:", value="AMIN1995")
    if st.button("إنشاء الاستيكر"):
        if q_text.strip() != "":
            img = qrcode.make(q_text)
            img.save("qrcode_gen.png")
            st.image("qrcode_gen.png", width=250)
            st.success("تم توليد الـ QR Code بنجاح وجاهز للطباعة واللزق.")
        else:
            st.warning("الرجاء إدخال الكود أولاً.")

# 4. العملاء
with tabs[3]:
    st.subheader("👥 العملاء")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_client_orig", clear_on_submit=True):
        c_name = st.text_input("اسم العميل:")
        c_phone = st.text_input("رقم الهاتف:")
        c_addr = st.text_input("العنوان:")
        c_interest = st.text_input("الاهتمام / الطلب:")
        if st.form_submit_button("حفظ العميل"):
            conn.execute("INSERT INTO clients (name, phone, address, interest) VALUES (?,?,?,?)", (c_name, c_phone, c_addr, c_interest))
            conn.commit(); st.rerun()
    df_c = pd.read_sql("SELECT * FROM clients", conn)
    st.dataframe(df_c, use_container_width=True)
    conn.close()

# 5. الصفقات
with tabs[4]:
    st.subheader("📈 الصفقات والمبيعات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_sale_orig", clear_on_submit=True):
        s_client = st.text_input("اسم العميل:")
        s_prod = st.text_input("اسم المنتج:")
        s_price = st.number_input("السعر الإجمالي:", min_value=0.0)
        s_qty = st.number_input("الكمية المباعة:", min_value=1, value=1)
        s_emp = st.text_input("الموظف المسؤول:")
        if st.form_submit_button("تسجيل الصفقة"):
            conn.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name) VALUES (?,?,?,?,?,?)",
                         (s_client, s_prod, s_price, s_qty, datetime.now().strftime("%Y-%m-%d"), s_emp))
            conn.commit(); st.rerun()
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    st.dataframe(df_s, use_container_width=True)
    conn.close()

# 6. التقارير
with tabs[5]:
    st.subheader("📊 التقارير التفصيلية")
    conn = sqlite3.connect(DB_PATH)
    df_sales = pd.read_sql("SELECT * FROM sales", conn)
    if not df_sales.empty:
        st.write("🏆 أكثر المنتجات مبيعاً:")
        st.bar_chart(df_sales.groupby('product_name')['quantity_sold'].sum())
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")
    conn.close()

# 7. الديون
with tabs[6]:
    st.subheader("💰 الديون والآجل")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_debt_orig", clear_on_submit=True):
        d_client = st.text_input("اسم العميل المدين:")
        d_rem = st.number_input("المبلغ المتبقي:", min_value=0.0)
        d_notes = st.text_input("ملاحظات:")
        if st.form_submit_button("حفظ الدين"):
            conn.execute("INSERT INTO debts (client_name, remaining, notes) VALUES (?,?,?)", (d_client, d_rem, d_notes))
            conn.commit(); st.rerun()
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    st.dataframe(df_d, use_container_width=True)
    conn.close()

# 8. المصروفات
with tabs[7]:
    st.subheader("💸 المصروفات والنثريات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_exp_orig", clear_on_submit=True):
        e_reason = st.text_input("سبب المصروف:")
        e_amount = st.number_input("المبلغ:", min_value=0.0)
        e_cat = st.selectbox("التصنيف:", ["نثريات", "إيجار", "نقل", "خامات", "أخرى"])
        if st.form_submit_button("تسجيل المصروف"):
            conn.execute("INSERT INTO expenses (reason, amount, category, date) VALUES (?,?,?,?)",
                         (e_reason, e_amount, e_cat, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df_e, use_container_width=True)
    conn.close()

# 9. المشاريع
with tabs[8]:
    st.subheader("🏗️ المشاريع والتشطيبات")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_proj_orig", clear_on_submit=True):
        p_name = st.text_input("اسم المشروع:")
        p_client = st.text_input("اسم العميل:")
        p_status = st.selectbox("الحالة:", ["جاري التنفيذ", "مكتمل", "مؤجل"])
        p_budget = st.number_input("الميزانية / القيمة:", min_value=0.0)
        if st.form_submit_button("حفظ المشروع"):
            conn.execute("INSERT INTO projects (project_name, client_name, status, budget) VALUES (?,?,?,?)",
                         (p_name, p_client, p_status, p_budget))
            conn.commit(); st.rerun()
    df_pr = pd.read_sql("SELECT * FROM projects", conn)
    st.dataframe(df_pr, use_container_width=True)
    conn.close()

# 10. الموظفين
with tabs[9]:
    st.subheader("🏅 الموظفون وفريق العمل")
    conn = sqlite3.connect(DB_PATH)
    with st.form("add_emp_orig", clear_on_submit=True):
        em_name = st.text_input("اسم الموظف:")
        em_role = st.text_input("التخصص / الوظيفة:")
        em_sal = st.number_input("الراتب:", min_value=0.0)
        em_phone = st.text_input("رقم الهاتف:")
        if st.form_submit_button("حفظ الموظف"):
            conn.execute("INSERT INTO employees (name, role, salary, phone) VALUES (?,?,?,?)", (em_name, em_role, em_sal, em_phone))
            conn.commit(); st.rerun()
    df_em = pd.read_sql("SELECT * FROM employees", conn)
    st.dataframe(df_em, use_container_width=True)
    conn.close()
