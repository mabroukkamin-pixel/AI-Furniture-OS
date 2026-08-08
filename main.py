import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "sovereign_100_matrix.db"
UPLOAD_FOLDER = "project_assets"

# التأكد من وجود مجلد الصور
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products_catalog 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT)''')
    try:
        c.execute("ALTER TABLE products_catalog ADD COLUMN category TEXT")
    except sqlite3.OperationalError:
        pass
        
    c.execute('''CREATE TABLE IF NOT EXISTS clients 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, interest TEXT, notes TEXT)''')
                 
    c.execute('''CREATE TABLE IF NOT EXISTS sales 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT)''')
    try:
        c.execute("ALTER TABLE sales ADD COLUMN employee_name TEXT")
    except sqlite3.OperationalError:
        pass
        
    c.execute('''CREATE TABLE IF NOT EXISTS debts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, phone TEXT, total_amount REAL, paid_amount REAL, remaining REAL, status TEXT)''')
    try:
        c.execute("ALTER TABLE debts ADD COLUMN phone TEXT")
    except sqlite3.OperationalError:
        pass
        
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, date TEXT)''')
                 
    c.execute('''CREATE TABLE IF NOT EXISTS projects 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT, total_cost REAL, paid_cost REAL, notes TEXT, before_img TEXT, after_img TEXT)''')
    try:
        c.execute("ALTER TABLE projects ADD COLUMN before_img TEXT")
        c.execute("ALTER TABLE projects ADD COLUMN after_img TEXT")
    except sqlite3.OperationalError:
        pass
        
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="centered")

# ==========================================
# 📱 وضع تطبيق الموبايل المصغر (ميداني) بجوار العنوان الأعلى
# ==========================================
col_title, col_mobile = st.columns([3, 1])
with col_title:
    st.title("🛒 سوق المروة للأثاث والديكور")
with col_mobile:
    with st.expander("📱 واجهة الميدان"):
        mobile_action = st.radio("اختر العملية:", ["تسجيل صفقة", "تسجيل مصروف"])
        
        if mobile_action == "تسجيل مصروف":
            with st.form("mobile_expense_form", clear_on_submit=True):
                m_reason = st.text_input("بيان المصروف:")
                m_amount = st.number_input("القيمة:", value=0.0, min_value=0.0)
                if st.form_submit_button("حفظ"):
                    if m_reason.strip() and m_amount > 0:
                        conn_m = sqlite3.connect(DB_PATH)
                        conn_m.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (f"[ميداني] {m_reason}", m_amount, datetime.now().strftime("%Y-%m-%d")))
                        conn_m.commit()
                        conn_m.close()
                        st.success("✅ تم الحفظ!")
                        st.rerun()
                    else:
                        st.error("⚠️ أدخل البيانات.")
        
        elif mobile_action == "تسجيل صفقة":
            conn_m = sqlite3.connect(DB_PATH)
            m_products = pd.read_sql("SELECT name, price, quantity FROM products_catalog WHERE quantity > 0", conn_m)
            m_emps = pd.read_sql("SELECT name FROM employees", conn_m)['name'].tolist()
            conn_m.close()
            
            if not m_products.empty and m_emps:
                with st.form("mobile_sale_form", clear_on_submit=True):
                    m_client = st.text_input("العميل:")
                    m_emp = st.selectbox("الموظف:", m_emps)
                    m_prod = st.selectbox("المنتج:", m_products['name'].tolist())
                    m_qty = st.number_input("الكمية:", min_value=1, value=1, step=1)
                    
                    if st.form_submit_button("إتمام البيع"):
                        conn_m2 = sqlite3.connect(DB_PATH)
                        cur_m = conn_m2.cursor()
                        p_row = cur_m.execute("SELECT id, quantity, price FROM products_catalog WHERE name = ?", (m_prod,)).fetchone()
                        if p_row and m_qty <= p_row[1]:
                            new_q = p_row[1] - m_qty
                            tot_p = p_row[2] * m_qty
                            cur_m.execute("UPDATE products_catalog SET quantity = ? WHERE id = ?", (new_q, p_row[0]))
                            cur_m.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name) VALUES (?,?,?,?,?,?)",
                                          (m_client if m_client else "عميل نقدي", m_prod, tot_p, m_qty, datetime.now().strftime("%Y-%m-%d %H:%M"), m_emp))
                            conn_m2.commit()
                            conn_m2.close()
                            st.success("🎉 تم البيع!")
                            st.rerun()
                        else:
                            st.error("⚠️ الكمية غير متوفرة.")
                            conn_m2.close()
            else:
                st.warning("⚠️ تأكد من وجود منتجات وموظفين.")

st.divider()

# ==========================================
# 🎛️ نظام الشبكة المربعة (Grid Menu) مع الأيقونات المطابقة للصورة
# ==========================================
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "📊 المؤشرات"

# القائمة مع الأيقونات تماماً كما تظهر في الواجهة الرسومية
tabs_dict = {
    "📊 المؤشرات": "📊 المؤشرات", 
    "📦 المخزون": "📦 المخزون", 
    "👥 العملاء": "👥 العملاء", 
    "📈 الصفقات": "📈 الصفقات", 
    "📊 التقارير": "📊 التقارير", 
    "💰 دفتر الآجل": "💰 دفتر الآجل", 
    "💸 المصروفات": "💸 المصروفات", 
    "🧾 الفواتير": "🧾 الفواتير", 
    "🏗️ المشاريع": "🏗️ المشاريع", 
    "🏅 الموظفين": "🏅 الموظفين"
}

tabs_list = list(tabs_dict.keys())

# ترتيب الأزرار في شبكة من 3 أعمدة
cols_num = 3
rows_count = len(tabs_list) // cols_num + (1 if len(tabs_list) % cols_num != 0 else 0)

idx = 0
for r in range(rows_count):
    cols = st.columns(cols_num)
    for c in range(cols_num):
        if idx < len(tabs_list):
            tab_key = tabs_list[idx]
            with cols[c]:
                if st.button(tab_key, use_container_width=True):
                    st.session_state.nav_tab = tab_key
                    st.rerun()
            idx += 1

st.markdown(f"### أنت الآن في: **{st.session_state.nav_tab}**")
st.divider()

main_categories = [
    "أثاث التخزين (كبتات وخزانات)",
    "أثاث الجلوس (كنب وكراسي)",
    "الطاولات والمكاتب",
    "استاندات وعرض",
    "ديكور وإضاءة",
    "مفروشات ونوم",
    "منوعات ومواسم"
]

current_page = st.session_state.nav_tab

# ----------------- تبويب: المؤشرات -----------------
if current_page == "📊 المؤشرات":
    st.subheader("📊 لوحة المؤشرات والتحليلات المرئية")
    
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    tot_sales = df_s['price'].sum() if not df_s.empty else 0.0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0.0
    net_profit = tot_sales - tot_exp
    total_debts = df_d['remaining'].sum() if not df_d.empty else 0.0
    
    c1, c2 = st.columns(2)
    c1.metric("💰 المبيعات", f"{tot_sales:,.1f} د.ك")
    c2.metric("💸 المصروفات", f"{tot_exp:,.1f} د.ك")
    c3, c4 = st.columns(2)
    c3.metric("📈 صافي العائد", f"{net_profit:,.1f} د.ك")
    c4.metric("⚠️ الديون", f"{total_debts:,.1f} د.ك")
    
    st.divider()
    if not df_s.empty and 'employee_name' in df_s.columns:
        st.markdown("### 🏆 مبيعات الموظفين")
        st.bar_chart(df_s.groupby('employee_name')['price'].sum())
    if not df_s.empty:
        st.markdown("### 📦 حركة المنتجات")
        st.bar_chart(df_s.groupby('product_name')['quantity_sold'].sum())

# ----------------- تبويب: المخزون -----------------
elif current_page == "📦 المخزون":
    st.subheader("📦 إدارة المخزون والفئات المنظمة")
    
    with st.expander("➕ إضافة منتج جديد"):
        with st.form("add_prod", clear_on_submit=True):
            category = st.selectbox("الفئة الرئيسية:", main_categories)
            name = st.text_input("اسم المنتج التفصيلي:")
            color = st.text_input("اللون:")
            dims = st.text_input("المقاسات:")
            price = st.number_input("السعر:", value=0.0)
            quantity = st.number_input("العدد المتوفر:", value=0, step=1)
            location = st.selectbox("الفرع:", ["سوق المروة", "السوق الصيني"])
            
            if st.form_submit_button("حفظ المنتج"):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO products_catalog (category, name, color, dims, price, quantity, location) VALUES (?,?,?,?,?,?,?)", 
                             (category, name, color, dims, price, quantity, location))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ المنتج!")
                st.rerun()

    with st.expander("✏️ تعديل أو حذف منتج"):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        all_products_db = conn.execute("SELECT * FROM products_catalog").fetchall()
        if all_products_db:
            prod_names = [p['name'] for p in all_products_db]
            selected_prod_name = st.selectbox("اختر المنتج:", prod_names)
            product = conn.execute("SELECT * FROM products_catalog WHERE name = ?", (selected_prod_name,)).fetchone()
            if product:
                with st.form("edit_delete_prod"):
                    new_category = st.selectbox("الفئة:", main_categories, index=main_categories.index(product['category']) if product['category'] in main_categories else 0)
                    new_price = st.number_input("السعر:", value=float(product["price"] or 0.0))
                    new_qty = st.number_input("الكمية:", value=int(product["quantity"] or 0), step=1)
                    new_dims = st.text_input("المقاسات:", value=str(product["dims"] or ""))
                    
                    c_b1, c_b2 = st.columns(2)
                    upd = c_b1.form_submit_button("حفظ")
                    dlt = c_b2.form_submit_button("حذف")
                    
                    if upd:
                        conn.execute("UPDATE products_catalog SET category=?, price=?, quantity=?, dims=? WHERE id=?", (new_category, new_price, new_qty, new_dims, product['id']))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم التحديث!")
                        st.rerun()
                    if dlt:
                        conn.execute("DELETE FROM products_catalog WHERE id=?", (product['id'],))
                        conn.commit()
                        conn.close()
                        st.warning("🗑️ تم الحذف!")
                        st.rerun()
        conn.close()

    st.divider()
    conn = sqlite3.connect(DB_PATH)
    all_data = pd.read_sql("SELECT id AS 'ID', category AS 'الفئة', name AS 'المنتج', color AS 'اللون', dims AS 'المقاسات', price AS 'السعر', quantity AS 'الكمية', location AS 'الفرع' FROM products_catalog", conn)
    conn.close()

    if not all_data.empty:
        selected_cat = st.selectbox("🔍 تصفية بالفئة:", ["الكل"] + list(all_data['الفئة'].dropna().unique()))
        df_filtered = all_data if selected_cat == "الكل" else all_data[all_data['الفئة'] == selected_cat]
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.info("لا توجد منتجات.")

# ----------------- تبويب: العملاء -----------------
elif current_page == "👥 العملاء":
    st.subheader("👥 بنك العملاء")
    with st.form("add_client", clear_on_submit=True):
        c_name = st.text_input("اسم العميل:")
        c_phone = st.text_input("رقم الهاتف:")
        c_interest = st.text_input("الاهتمام:")
        c_notes = st.text_input("ملاحظات:")
        if st.form_submit_button("حفظ العميل"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO clients (name, phone, interest, notes) VALUES (?,?,?,?)", (c_name, c_phone, c_interest, c_notes))
            conn.commit()
            conn.close()
            st.success("✅ تم الحفظ!")
            st.rerun()
            
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT name AS 'الاسم', phone AS 'الهاتف', interest AS 'الاهتمام', notes AS 'ملاحظات' FROM clients", conn), use_container_width=True)
    conn.close()

# ----------------- تبويب: الصفقات -----------------
elif current_page == "📈 الصفقات":
    st.subheader("📈 تسجيل صفقة بيع")
    conn = sqlite3.connect(DB_PATH)
    products_list = pd.read_sql("SELECT id, name, quantity, price FROM products_catalog WHERE quantity > 0", conn)
    emps_list = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
    conn.close()

    if not products_list.empty and emps_list:
        with st.form("make_sale", clear_on_submit=True):
            client_sale_name = st.text_input("اسم العميل:")
            selected_emp = st.selectbox("الموظف المسؤول:", emps_list)
            selected_prod_name = st.selectbox("المنتج:", products_list['name'].tolist())
            sold_qty = st.number_input("الكمية المباعة:", min_value=1, value=1, step=1)
            
            if st.form_submit_button("إتمام البيع"):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                prod_info = cursor.execute("SELECT id, quantity, price FROM products_catalog WHERE name = ?", (selected_prod_name,)).fetchone()
                if prod_info and sold_qty <= prod_info[1]:
                    cursor.execute("UPDATE products_catalog SET quantity = ? WHERE id = ?", (prod_info[1] - sold_qty, prod_info[0]))
                    cursor.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name) VALUES (?,?,?,?,?,?)", 
                                   (client_sale_name, selected_prod_name, prod_info[2] * sold_qty, sold_qty, datetime.now().strftime("%Y-%m-%d %H:%M"), selected_emp))
                    conn.commit()
                    conn.close()
                    st.success("🎉 تم البيع بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ الكمية غير متوفرة.")
                    conn.close()
    else:
        st.warning("⚠️ يرجى التأكد من إضافة موظفين ومنتجات متوفرة أولاً.")

    st.divider()
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT client_name AS 'العميل', employee_name AS 'الموظف', product_name AS 'المنتج', price AS 'الإجمالي', quantity_sold AS 'الكمية', date AS 'التاريخ' FROM sales", conn), use_container_width=True)
    conn.close()

# ----------------- تبويب: التقارير -----------------
elif current_page == "📊 التقارير":
    st.subheader("📊 التقارير المالية وتصدير البيانات")
    conn = sqlite3.connect(DB_PATH)
    df_sales_rep = pd.read_sql("SELECT * FROM sales", conn)
    df_exp_rep = pd.read_sql("SELECT * FROM expenses", conn)
    df_debts_rep = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    total_sales = df_sales_rep['price'].sum() if not df_sales_rep.empty else 0.0
    total_expenses = df_exp_rep['amount'].sum() if not df_exp_rep.empty else 0.0
    
    col1, col2 = st.columns(2)
    col1.metric("المبيعات", f"{total_sales} د.ك")
    col2.metric("المصروفات", f"{total_expenses} د.ك")
    st.metric("صافي الربح", f"{total_sales - total_expenses} د.ك")
    
    st.divider()
    if not df_sales_rep.empty:
        st.download_button("📥 تقرير المبيعات (CSV)", df_sales_rep.to_csv(index=False).encode('utf-8-sig'), "sales.csv", "text/csv")
    if not df_exp_rep.empty:
        st.download_button("📥 تقرير المصروفات (CSV)", df_exp_rep.to_csv(index=False).encode('utf-8-sig'), "expenses.csv", "text/csv")

# ----------------- تبويب: دفتر الآجل -----------------
elif current_page == "💰 دفتر الآجل":
    st.subheader("💰 دفتر الحسابات والآجل")
    with st.expander("➕ تسجيل آجل أو عربون"):
        with st.form("add_debt", clear_on_submit=True):
            d_name = st.text_input("اسم العميل:")
            d_phone = st.text_input("الهاتف:")
            d_total = st.number_input("الإجمالي:", value=0.0)
            d_paid = st.number_input("المدفوع (العربون):", value=0.0)
            if st.form_submit_button("حفظ الحساب"):
                rem = d_total - d_paid
                st_val = "خالص" if rem <= 0 else "متبقي"
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO debts (client_name, phone, total_amount, paid_amount, remaining, status) VALUES (?,?,?,?,?,?)", (d_name, d_phone, d_total, d_paid, rem, st_val))
                conn.commit()
                conn.close()
                st.success("✅ تم الحفظ!")
                st.rerun()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    active_debts = conn.execute("SELECT * FROM debts WHERE status = 'متبقي'").fetchall()
    conn.close()
    
    if active_debts:
        for d in active_debts:
            st.error(f"👤 {d['client_name']} | المتبقي: **{d['remaining']} د.ك**")
            if d['phone']:
                wa_msg = f"السلام عليكم، تذكرة من سوق المروة بالمبلغ المتبقي {d['remaining']} د.ك."
                st.markdown(f'<a href="https://wa.me/{d["phone"]}?text={wa_msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:5px 10px; border-radius:5px;">💬 واتساب</button></a>', unsafe_allow_html=True)
    else:
        st.success("🎉 لا توجد ديون مستحقة.")

# ----------------- تبويب: المصروفات -----------------
elif current_page == "💸 المصروفات":
    st.subheader("💸 المصروفات اليومية")
    with st.form("add_expense", clear_on_submit=True):
        reason = st.text_input("سبب المصروف:")
        amount = st.number_input("القيمة:", value=0.0)
        if st.form_submit_button("تسجيل المصروف"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (reason, amount, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("✅ تم التسجيل!")
            st.rerun()
            
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT reason AS 'السبب', amount AS 'المبلغ', date AS 'التاريخ' FROM expenses", conn), use_container_width=True)
    conn.close()

# ----------------- تبويب: الفواتير -----------------
elif current_page == "🧾 الفواتير":
    st.subheader("🧾 الفواتير والإيصالات")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    debts_for_invoice = conn.execute("SELECT * FROM debts").fetchall()
    conn.close()
    
    if debts_for_invoice:
        inv_options = {f"عميل: {d['client_name']} (المتبقي: {d['remaining']})": d for d in debts_for_invoice}
        selected_inv_label = st.selectbox("اختر العميل للإيصال:", list(inv_options.keys()))
        chosen_inv = inv_options[selected_inv_label]
        
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #f9f9f9; color: #000;">
            <h3 style="text-align: center; color: #2E7D32;">🛒 سوق المروة للأثاث والديكور</h3>
            <hr>
            <p><b>رقم الإيصال:</b> #{chosen_inv['id']}</p>
            <p><b>العميل:</b> {chosen_inv['client_name']}</p>
            <p><b>الإجمالي:</b> {chosen_inv['total_amount']} د.ك</p>
            <p><b>المدفوع:</b> {chosen_inv['paid_amount']} د.ك</p>
            <p><b>المتبقي:</b> <span style="color: red;">{chosen_inv['remaining']} د.ك</span></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("لا توجد فواتير مسجلة.")

# ----------------- تبويب: المشاريع -----------------
elif current_page == "🏗️ المشاريع":
    st.subheader("🏗️ مشاريع التنفيذ والتشطيب")
    with st.expander("➕ إضافة مشروع جديد"):
        with st.form("add_proj", clear_on_submit=True):
            p_name = st.text_input("اسم المشروع:")
            c_name = st.text_input("اسم العميل:")
            status = st.selectbox("المرحلة:", ["تأسيس", "معجون", "دهان أولي", "تشطيب نهائي", "تسليم"])
            total_cost = st.number_input("التكلفة الإجمالية:", value=0.0)
            paid_cost = st.number_input("المحصل:", value=0.0)
            notes = st.text_area("ملاحظات:")
            b_img = st.file_uploader("صورة قبل:", type=['jpg', 'png'])
            a_img = st.file_uploader("صورة بعد:", type=['jpg', 'png'])
            
            if st.form_submit_button("حفظ المشروع"):
                b_path, a_path = None, None
                if b_img:
                    b_path = os.path.join(UPLOAD_FOLDER, f"before_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
                    with open(b_path, "wb") as f: f.write(b_img.getbuffer())
                if a_img:
                    a_path = os.path.join(UPLOAD_FOLDER, f"after_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
                    with open(a_path, "wb") as f: f.write(a_img.getbuffer())
                
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO projects (project_name, client_name, status, total_cost, paid_cost, notes, before_img, after_img) VALUES (?,?,?,?,?,?,?,?)",
                             (p_name, c_name, status, total_cost, paid_cost, notes, b_path, a_path))
                conn.commit()
                conn.close()
                st.success("✅ تم الحفظ!")
                st.rerun()

    conn = sqlite3.connect(DB_PATH)
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    if projects:
        for p in projects:
            st.markdown(f"**المشروع:** {p[1]} | **العميل:** {p[2]} | **المرحلة:** {p[3]}")
    else:
        st.info("لا توجد مشاريع.")

# ----------------- تبويب: الموظفين -----------------
elif current_page == "🏅 الموظفين":
    st.subheader("🏅 أداء الموظفين")
    with st.form("add_emp", clear_on_submit=True):
        emp_name = st.text_input("اسم الموظف الجديد:")
        if st.form_submit_button("حفظ الموظف"):
            if emp_name.strip():
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO employees (name) VALUES (?)", (emp_name,))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ الموظف!")
                st.rerun()
                
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT name AS 'اسم الموظف' FROM employees", conn), use_container_width=True)
    conn.close()
