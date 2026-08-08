import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# ======================================================================
# 💡 CSS لتثبيت شريط الـ Tabs في أعلى الشاشة دائمًا (Sticky)
# ======================================================================
st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child {
        position: fixed !important;
        top: 50px !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #ffffff;
        z-index: 99999;
        padding: 10px 20px 0px 20px;
        border-bottom: 2px solid #f0f2f6;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stTabs"] > div:nth-child(2) {
        padding-top: 70px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد قاعدة البيانات والمسارات
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
    
    # التأكد من الأعمدة
    c.execute("PRAGMA table_info(sales)")
    columns = [col[1] for col in c.fetchall()]
    if 'status' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN status TEXT DEFAULT 'مكتملة'")
    if 'cancel_reason' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN cancel_reason TEXT DEFAULT ''")
    if 'payment_method' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN payment_method TEXT DEFAULT 'كاش'")
    if 'employee_name' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN employee_name TEXT DEFAULT ''")
    if 'branch' not in columns:
        c.execute("ALTER TABLE sales ADD COLUMN branch TEXT DEFAULT 'سوق المروة'")

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
st.write("أهلاً بك يا أمين، نظام الإدارة والتشغيل الشامل.")

# 4. شريط الأقسام العلوي الثابت
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
    st.subheader("📦 إدارة المخزون والفئات المنظمة للمنتجات")
    
    # جلب المنتجات المتاحة من قاعدة البيانات
    conn = sqlite3.connect(DB_PATH)
    try:
        df_all_prod = pd.read_sql("SELECT * FROM products_catalog", conn)
    except:
        df_all_prod = pd.DataFrame()
    conn.close()

    if not df_all_prod.empty:
        # إعادة تسمية الأعمدة لعرضها بشكل احترافي وجميل
        display_df = df_all_prod.rename(columns={
            'id': 'رقم ID',
            'category': 'الفئة',
            'name': 'المنتج',
            'color': 'اللون',
            'dims': 'المقاسات',
            'price': 'السعر',
            'quantity': 'الكمية',
            'location': 'الفرع',
            'barcode': 'الباركود'
        })
        
        selected_filter_cat = st.selectbox("🔍 تصفية الجدول حسب الفئة:", ["الكل (عرض كل الفئات)"] + main_categories)
        if selected_filter_cat != "الكل (عرض كل الفئات)":
            filtered_df = display_df[display_df['الفئة'] == selected_filter_cat]
        else:
            filtered_df = display_df
            
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("⚠️ لا توجد منتجات مسجلة في المخزون حتى الآن. يمكنك إضافة منتج جديد باستخدام النمط أدناه.")

    st.markdown("---")
    st.subheader("➕ إضافة منتج جديد بالمخزون")
    with st.form("add_prod", clear_on_submit=True):
        category = st.selectbox("الفئة الرئيسية:", main_categories)
        name = st.text_input("اسم المنتج التفصيلي:")
        color = st.text_input("اللون:")
        dims = st.text_input("المقاسات:")
        price = st.number_input("السعر (د.ك):", value=0.0, min_value=0.0)
        quantity = st.number_input("العدد المتوفر:", value=1, step=1, min_value=0)
        location = st.selectbox("الفرع:", ["سوق المروة", "السوق الصيني"])
        barcode = st.text_input("كود الباركود (اختياري):")
        
        if st.form_submit_button("حفظ المنتج بالكامل"):
            if name.strip() == "":
                st.error("⚠️ يرجى كتابة اسم المنتج على الأقل.")
            else:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO products_catalog (category, name, color, dims, price, quantity, location, barcode) VALUES (?,?,?,?,?,?,?,?)", 
                           (category, name, color, dims, price, quantity, location, barcode))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ المنتج بنجاح!")
                st.rerun()

# ----------------- 3. العملاء -----------------
with tabs[2]:
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
with tabs[3]:
    st.subheader("📈 تسجيل صفقة بيع جديدة وإدارتها")
    conn = sqlite3.connect(DB_PATH)
    try: products_list = pd.read_sql("SELECT id, name, quantity, price FROM products_catalog WHERE quantity > 0", conn)
    except: products_list = pd.DataFrame()
    try: emps_list = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
    except: emps_list = []
    try: df_sales_manage = pd.read_sql("SELECT * FROM sales", conn)
    except: df_sales_manage = pd.DataFrame()
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
        st.warning("⚠️ لتمكين الصفقات، يرجى إضافة موظفين في قسم 'الموظفين' ومنتجات متوفرة بالمخزون أولاً.")

    st.markdown("---")
    st.subheader("📋 سجل الصفقات وإلغائها عند الضرورة")
    if not df_sales_manage.empty:
        st.dataframe(df_sales_manage, use_container_width=True)
    else:
        st.info("لا توجد صفقات مسجلة.")

# ----------------- 5. التقارير -----------------
with tabs[4]:
    st.subheader("📊 تقارير المبيعات والأداء")
    conn = sqlite3.connect(DB_PATH)
    try: df_sales_rep = pd.read_sql("SELECT * FROM sales", conn)
    except: df_sales_rep = pd.DataFrame()
    conn.close()
    if not df_sales_rep.empty:
        st.dataframe(df_sales_rep, use_container_width=True)
        st.download_button("📥 تحميل تقرير المبيعات (CSV)", df_sales_rep.to_csv(index=False).encode('utf-8-sig'), "sales_report.csv", "text/csv")
    else:
        st.info("لا توجد مبيعات مسجلة حالياً.")

# ----------------- 6. دفتر الآجل والديون -----------------
with tabs[5]:
    st.subheader("💰 إدارة الديون والآجل وعربون العملاء")
    conn = sqlite3.connect(DB_PATH)
    try: df_debts_all = pd.read_sql("SELECT * FROM debts", conn)
    except: df_debts_all = pd.DataFrame()
    conn.close()
    
    if not df_debts_all.empty:
        st.dataframe(df_debts_all, use_container_width=True)
        with st.form("pay_debt_form"):
            debt_id = st.selectbox("اختر رقم الدين لتسجيل سداد:", df_debts_all['id'].tolist())
            pay_add = st.number_input("المبلغ المراد سداده الآن (د.ك):", min_value=0.0)
            if st.form_submit_button("تحديث السداد"):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                row = cur.execute("SELECT paid_amount, total_amount FROM debts WHERE id = ?", (debt_id,)).fetchone()
                if row:
                    new_paid = row[0] + pay_add
                    new_rem = row[1] - new_paid
                    status = "مخلص" if new_rem <= 0 else "متبقي"
                    cur.execute("UPDATE debts SET paid_amount = ?, remaining = ?, status = ? WHERE id = ?", (new_paid, max(0.0, new_rem), status, debt_id))
                    conn.commit()
                conn.close()
                st.success("✅ تم تحديث الدين بنجاح!")
                st.rerun()
    else:
        st.info("لا توجد ديون مسجلة.")

# ----------------- 7. المصروفات -----------------
with tabs[6]:
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
with tabs[7]:
    st.subheader("🧾 طباعة وعرض الفواتير الرسمية")
    conn = sqlite3.connect(DB_PATH)
    try: sales_invoices = pd.read_sql("SELECT * FROM sales", conn)
    except: sales_invoices = pd.DataFrame()
    conn.close()
    if not sales_invoices.empty:
        sel_inv_id = st.selectbox("اختر رقم الفاتورة للطباعة:", sales_invoices['id'].tolist())
        inv_data = sales_invoices[sales_invoices['id'] == sel_inv_id].iloc[0]
        
        c_name = inv_data.get('client_name', 'عميل')
        p_name = inv_data.get('product_name', 'منتج')
        qty = inv_data.get('quantity_sold', 1)
        pay_m = inv_data.get('payment_method', 'كاش')
        price_val = inv_data.get('price', 0.0)
        inv_date = inv_data.get('date', '')

        st.markdown(f"""
        <div style="border: 2px dashed #333; padding: 20px; border-radius: 10px; background-color: #fafafa; color: #000;">
            <h2 style="text-align: center;">سوق المروة للأثاث والديكور</h2>
            <p style="text-align: center;">فرع الكويت - الفاتورة الرسمية</p>
            <hr>
            <p><b>رقم الفاتورة:</b> #{sel_inv_id}</p>
            <p><b>التاريخ:</b> {inv_date}</p>
            <p><b>اسم العميل:</b> {c_name}</p>
            <p><b>المنتج:</b> {p_name}</p>
            <p><b>الكمية:</b> {qty}</p>
            <p><b>طريقة الدفع:</b> {pay_m}</p>
            <h3 style="text-align: left;">الإجمالي: {price_val} د.ك</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("لا توجد فواتير متاحة.")

# ----------------- 9. المشاريع -----------------
with tabs[8]:
    st.subheader("🏗️ إدارة المشاريع والديكورات")
    with st.form("add_project", clear_on_submit=True):
        p_name = st.text_input("اسم المشروع:")
        p_client = st.text_input("اسم العميل:")
        p_cost = st.number_input("تكلفة المشروع الإجمالية:", min_value=0.0)
        p_paid = st.number_input("المبلغ المدفوع مقدماً:", min_value=0.0)
        p_team = st.text_input("فريق العمل المنفذ:")
        p_notes = st.text_area("ملاحظات المشروع:")
        if st.form_submit_button("حفظ المشروع"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO projects (project_name, client_name, status, total_cost, paid_cost, notes, team, deadline) VALUES (?,?,?,?,?,?,?,?)",
                         (p_name, p_client, "قيد التنفيذ", p_cost, p_paid, p_notes, p_team, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("✅ تم حفظ المشروع بنجاح!")
            st.rerun()
    conn = sqlite3.connect(DB_PATH)
    try: st.dataframe(pd.read_sql("SELECT * FROM projects", conn), use_container_width=True)
    except: pass
    conn.close()

# ----------------- 10. الموظفين -----------------
with tabs[9]:
    st.subheader("🏅 إدارة الموظفين والشؤون الداخلية")
    emp_sub_tab1, emp_sub_tab2 = st.tabs(["بيانات الموظفين والرواتب", "حضور وسلف الموظفين"])
    
    with emp_sub_tab1:
        with st.form("add_emp", clear_on_submit=True):
            e_name = st.text_input("اسم الموظف الكامل:")
            e_phone = st.text_input("رقم الهاتف:")
            e_role = st.text_input("الوظيفة / التخصص:")
            e_salary = st.number_input("الراتب الأساسي:", min_value=0.0)
            if st.form_submit_button("حفظ الموظف"):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO employees (name, phone, address, hire_date, role, salary) VALUES (?,?,?,?,?,?)",
                             (e_name, e_phone, "الكويت", datetime.now().strftime("%Y-%m-%d"), e_role, e_salary))
                conn.commit()
                conn.close()
                st.success("✅ تم تسجيل الموظف!")
                st.rerun()
        conn = sqlite3.connect(DB_PATH)
        try: st.dataframe(pd.read_sql("SELECT * FROM employees", conn), use_container_width=True)
        except: pass
        conn.close()

    with emp_sub_tab2:
        conn = sqlite3.connect(DB_PATH)
        try: emps_names = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
        except: emps_names = []
        conn.close()

        if emps_names:
            with st.form("bonus_form", clear_on_submit=True):
                b_emp = st.selectbox("الموظف:", emps_names)
                b_amt = st.number_input("قيمة المكافأة أو السلفة:", min_value=0.0)
                b_reason = st.text_input("السبب:")
                if st.form_submit_button("تسجيل مكافأة / سلفة"):
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO employee_bonuses (employee_name, amount, reason, date) VALUES (?,?,?,?)",
                                 (b_emp, b_amt, b_reason, datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    conn.close()
                    st.success("✅ تمت الإضافة!")
                    st.rerun()
            conn = sqlite3.connect(DB_PATH)
            try: st.dataframe(pd.read_sql("SELECT * FROM employee_bonuses", conn), use_container_width=True)
            except: pass
            conn.close()
        else:
            st.info("الرجاء إضافة موظفين أولاً.")
