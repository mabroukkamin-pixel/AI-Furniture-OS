import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

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

# 3. العنوان الرئيسي للبرنامج في الواجهة
st.title("🛒 سوق المروة للأثاث والديكور - النظام المتكامل")
st.write("أهلاً بك يا أمين، نظام الإدارة والتشغيل السريع.")
st.divider()

# 4. قائمة الأقسام المتاحة
pages_list = [
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
]

# استخدام نظام القائمة المنسدلة الذكية أو الاختيار المرن لتناسب الموبايل والشاشات الصغيرة تماماً بدلاً من شريط الأزرار المزدحم
st.markdown("### 📌 لوحة التحكم السريعة - اختر القسم المطلوب:")

# تقسيم الأقسام على أزرار مرتبة بصفوف (Grid) لسهولة الضغط عليها من الموبايل
cols_per_row = 3
rows = [pages_list[i:i + cols_per_row] for i in range(0, len(pages_list), cols_per_row)]

# حفظ القسم الحالي في جلسة التصفح
if 'current_page' not in st.session_state:
    st.session_state.current_page = "📊 المؤشرات"

for row in rows:
    cols = st.columns(len(row))
    for idx, page_name in enumerate(row):
        with cols[idx]:
            if st.button(page_name, use_container_width=True):
                st.session_state.current_page = page_name

current_page = st.session_state.current_page
st.markdown(f"--- \n ## 📂 القسم الحالي: {current_page}")

# ----------------- 1. المؤشرات -----------------
if current_page == "📊 المؤشرات":
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
elif current_page == "📦 المخزون":
    st.subheader("📦 إدارة المخزون والفئات المنظمة للمنتجات")
    conn = sqlite3.connect(DB_PATH)
    try:
        df_all_prod = pd.read_sql("SELECT id AS 'رقم ID', category AS 'الفئة', name AS 'المنتج', color AS 'اللون', dims AS 'المقاسات', price AS 'السعر', quantity AS 'الكمية', location AS 'الفرع', barcode AS 'الباركود' FROM products_catalog", conn)
    except:
        df_all_prod = pd.DataFrame()
    conn.close()

    if not df_all_prod.empty:
        selected_filter_cat = st.selectbox("🔍 تصفية الجدول حسب الفئة:", ["الكل (عرض كل الفئات)"] + main_categories)
        if selected_filter_cat != "الكل (عرض كل الفئات)":
            filtered_df = df_all_prod[df_all_prod['الفئة'] == selected_filter_cat]
        else:
            filtered_df = df_all_prod
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("لا توجد منتجات مسجلة بعد.")

    with st.expander("➕ إضافة منتج جديد بالمخزون"):
        with st.form("add_prod", clear_on_submit=True):
            category = st.selectbox("الفئة الرئيسية:", main_categories)
            name = st.text_input("اسم المنتج التفصيلي:")
            color = st.text_input("اللون:")
            dims = st.text_input("المقاسات:")
            price = st.number_input("السعر:", value=0.0, min_value=0.0)
            quantity = st.number_input("العدد المتوفر:", value=0, step=1, min_value=0)
            location = st.selectbox("الفرع:", ["سوق المروة", "السوق الصيني"])
            barcode = st.text_input("كود الباركود:")
            
            if st.form_submit_button("حفظ المنتج بالكامل"):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO products_catalog (category, name, color, dims, price, quantity, location, barcode) VALUES (?,?,?,?,?,?,?,?)", 
                           (category, name, color, dims, price, quantity, location, barcode))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ المنتج بنجاح!")
                st.rerun()

# ----------------- 3. العملاء -----------------
elif current_page == "👥 العملاء":
    st.subheader("👥 إدارة العملاء وعلاقاتهم (CRM)")
    with st.form("add_client", clear_on_submit=True):
        c_name = st.text_input("اسم العميل:")
        c_phone = st.text_input("رقم الهاتف:")
        c_interest = st.text_input("اهتمامات العميل والديكورات المفضلة:")
        c_notes = st.text_input("ملاحظات إضافية:")
        if st.form_submit_button("حفظ ملف العميل"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO clients (name, phone, interest, notes) VALUES (?,?,?,?)", (c_name, c_phone, c_interest, c_notes))
            conn.commit()
            conn.close()
            st.success("✅ تم حفظ ملف العميل بنجاح!")
            st.rerun()
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT name AS 'اسم العميل', phone AS 'الهاتف', interest AS 'الاهتمامات', notes AS 'ملاحظات' FROM clients", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 4. الصفقات -----------------
elif current_page == "📈 الصفقات":
    st.subheader("📈 تسجيل صفقة بيع جديدة")
    conn = sqlite3.connect(DB_PATH)
    try: products_list = pd.read_sql("SELECT id, name, quantity, price FROM products_catalog WHERE quantity > 0", conn)
    except: products_list = pd.DataFrame()
    try: emps_list = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
    except: emps_list = []
    conn.close()

    if not products_list.empty and emps_list:
        with st.form("make_sale", clear_on_submit=True):
            client_sale_name = st.text_input("اسم العميل:")
            client_phone_sale = st.text_input("رقم هاتف العميل:")
            selected_emp = st.selectbox("الموظف المسؤول:", emps_list)
            selected_prod_name = st.selectbox("المنتج:", products_list['name'].tolist())
            sold_qty = st.number_input("الكمية المباعة:", min_value=1, value=1, step=1)
            payment_method = st.selectbox("طريقة الدفع:", ["كاش", "شبكة KNET", "تحويل بنكي", "آجل / عربون"])
            branch_select = st.selectbox("فرع البيع:", ["سوق المروة", "السوق الصيني"])
            
            paid_deposit = 0.0
            if payment_method == "آجل / عربون":
                paid_deposit = st.number_input("قيمة العربون المدفوع حالياً (د.ك):", value=0.0, min_value=0.0)

            if st.form_submit_button("إتمام الصفقة وتسجيل البيع"):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                prod_info = cursor.execute("SELECT id, quantity, price FROM products_catalog WHERE name = ?", (selected_prod_name,)).fetchone()
                
                if prod_info and sold_qty <= prod_info[1]:
                    cursor.execute("UPDATE products_catalog SET quantity = ? WHERE id = ?", (prod_info[1] - sold_qty, prod_info[0]))
                    total_amt_sale = prod_info[2] * sold_qty
                    
                    cursor.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name, payment_method, branch, status, cancel_reason) VALUES (?,?,?,?,?,?,?,?,?,?)", 
                                   (client_sale_name if client_sale_name else "عميل نقدي", selected_prod_name, total_amt_sale, sold_qty, datetime.now().strftime("%Y-%m-%d %H:%M"), selected_emp, payment_method, branch_select, "مكتملة", ""))
                    
                    if payment_method == "آجل / عربون" or paid_deposit < total_amt_sale:
                        remaining_amt = total_amt_sale - paid_deposit
                        cursor.execute("INSERT INTO debts (client_name, phone, total_amount, paid_amount, remaining, status, due_date) VALUES (?,?,?,?,?,?,?)",
                                       (client_sale_name if client_sale_name else "عميل آجل", client_phone_sale, total_amt_sale, paid_deposit, remaining_amt, "متبقي", datetime.now().strftime("%Y-%m-%d")))

                    conn.commit()
                    conn.close()
                    st.success("🎉 تمت الصفقة وتسجيلها بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ الكمية المطلوبة غير متوفرة.")
                    conn.close()
    else:
        st.warning("⚠️ يرجى إضافة موظفين ومنتجات متوفرة بالمخزون أولاً.")

# ----------------- 5. التقارير -----------------
elif current_page == "📊 التقارير":
    st.subheader("📊 تقارير المبيعات والأداء")
    conn = sqlite3.connect(DB_PATH)
    try: df_sales_rep = pd.read_sql("SELECT * FROM sales", conn)
    except: df_sales_rep = pd.DataFrame()
    conn.close()
    if not df_sales_rep.empty:
        st.dataframe(df_sales_rep, use_container_width=True)
        st.download_button("📥 تحميل تقرير المبيعات", df_sales_rep.to_csv(index=False).encode('utf-8-sig'), "sales_report.csv", "text/csv")
    else:
        st.info("لا توجد مبيعات مسجلة حالياً.")

# ----------------- 6. دفتر الآجل والديون -----------------
elif current_page == "💰 الآجل والديون":
    st.subheader("💰 إدارة الديون والآجل وعربون العملاء")
    conn = sqlite3.connect(DB_PATH)
    try: df_debts_all = pd.read_sql("SELECT * FROM debts", conn)
    except: df_debts_all = pd.DataFrame()
    conn.close()
    st.dataframe(df_debts_all, use_container_width=True)

# ----------------- 7. المصروفات -----------------
elif current_page == "💸 المصروفات":
    st.subheader("💸 إدارة المصروفات")
    with st.form("expense_form", clear_on_submit=True):
        reason = st.text_input("بيان المصروف:")
        amount = st.number_input("المبلغ:", value=0.0, min_value=0.0)
        category = st.selectbox("التصنيف:", ["نثريات", "إيجار", "رواتب", "نقل", "أخرى"])
        if st.form_submit_button("تسجيل المصروف"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO expenses (reason, amount, date, category) VALUES (?,?,?,?)",
                         (reason, amount, datetime.now().strftime("%Y-%m-%d"), category))
            conn.commit()
            conn.close()
            st.success("✅ تم التسجيل!")
            st.rerun()
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM expenses", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 8. الفواتير -----------------
elif current_page == "🧾 الفواتير":
    st.subheader("🧾 طباعة الفواتير")
    conn = sqlite3.connect(DB_PATH)
    try: sales_invoices = pd.read_sql("SELECT * FROM sales", conn)
    except: sales_invoices = pd.DataFrame()
    conn.close()
    if not sales_invoices.empty:
        sel_inv_id = st.selectbox("اختر رقم الفاتورة:", sales_invoices['id'].tolist())
        inv_data = sales_invoices[sales_invoices['id'] == sel_inv_id].iloc[0]
        st.write(f"فاتورة رقم: #{inv_data['id']} - العميل: {inv_data['client_name']} - الإجمالي: {inv_data['price']} د.ك")
    else:
        st.info("لا توجد فواتير.")

# ----------------- 9. المشاريع -----------------
elif current_page == "🏗️ المشاريع":
    st.subheader("🏗️ إدارة المشاريع")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM projects", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 10. الموظفين -----------------
elif current_page == "🏅 الموظفين":
    st.subheader("🏅 إدارة الموظفين")
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM employees", conn), use_container_width=True)
    except: pass
    conn.close()
