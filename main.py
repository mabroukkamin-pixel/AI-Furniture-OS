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

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# ==========================================
# 📱 وضع تطبيق الموبايل المصغر (ميداني) بجوار العنوان الأعلى
# ==========================================
col_title, col_mobile = st.columns([4, 1])
with col_title:
    st.title("🛒 سوق المروة للأثاث والديكور - لوحة الإدارة الشاملة")
with col_mobile:
    st.markdown("### 📱 وضع تطبيق الموبايل المصغر (ميداني)")
    with st.expander("فتح واجهة الموبايل المصغرة السريعة"):
        st.info("استخدم هذه الواجهة المبسطة أثناء تواجدك في موقع العمل لتسجيل المصروفات أو الصفقات سريعاً من هاتفك الذكي.")
        
        mobile_action = st.radio("اختر العملية المطلوبة:", ["تسجيل صفقة سريعة", "تسجيل مصروف يومي / عمالة"])
        
        if mobile_action == "تسجيل مصروف يومي / عمالة":
            with st.form("mobile_expense_form", clear_on_submit=True):
                m_reason = st.text_input("بيان المصروف (مثال: أجرة عمال، بنزين، خامات..)")
                m_amount = st.number_input("القيمة:", value=0.0, min_value=0.0)
                if st.form_submit_button("💾 حفظ المصروف فوراً"):
                    if m_reason.strip() and m_amount > 0:
                        conn_m = sqlite3.connect(DB_PATH)
                        conn_m.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (f"[ميداني] {m_reason}", m_amount, datetime.now().strftime("%Y-%m-%d")))
                        conn_m.commit()
                        conn_m.close()
                        st.success("✅ تم حفظ المصروف الميداني بنجاح!")
                        st.rerun()
                    else:
                        st.error("⚠️ يرجى إدخال البيان والقيمة.")
        
        elif mobile_action == "تسجيل صفقة سريعة":
            conn_m = sqlite3.connect(DB_PATH)
            m_products = pd.read_sql("SELECT name, price, quantity FROM products_catalog WHERE quantity > 0", conn_m)
            m_emps = pd.read_sql("SELECT name FROM employees", conn_m)['name'].tolist()
            conn_m.close()
            
            if not m_products.empty and m_emps:
                with st.form("mobile_sale_form", clear_on_submit=True):
                    m_client = st.text_input("اسم العميل:")
                    m_emp = st.selectbox("الموظف المسؤول:", m_emps)
                    m_prod = st.selectbox("المنتج:", m_products['name'].tolist())
                    m_qty = st.number_input("الكمية:", min_value=1, value=1, step=1)
                    
                    if st.form_submit_button("🚀 إتمام البيع السريع"):
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
                            st.success("🎉 تم تسجيل الصفقة الميدانية بنجاح!")
                            st.rerun()
                        else:
                            st.error("⚠️ الكمية غير متوفرة بالمخزون.")
                            conn_m2.close()
            else:
                st.warning("⚠️ يرجى التأكد من وجود منتجات بالمخزون وموظفين مسجلين أولاً.")

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 لوحة المؤشرات (Dashboard)", 
    "📦 المخزون", 
    "👥 العملاء", 
    "📈 الصفقات", 
    "📊 التقارير", 
    "💰 دفتر الآجل", 
    "💸 المصروفات", 
    "🧾 الفواتير", 
    "🏗️ مشاريع التنفيذ", 
    "🏅 أداء الموظفين"
])

main_categories = [
    "أثاث التخزين (كبتات وخزانات)",
    "أثاث الجلوس (كنب وكراسي)",
    "الطاولات والمكاتب",
    "استاندات وعرض",
    "ديكور وإضاءة",
    "مفروشات ونوم",
    "منوعات ومواسم"
]

# ----------------- تبويب 0: لوحة المؤشرات (Dashboard المرئية) -----------------
with tab0:
    st.subheader("📊 لوحة المؤشرات والتحليلات المرئية لسوق المروة")
    
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    tot_sales = df_s['price'].sum() if not df_s.empty else 0.0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0.0
    net_profit = tot_sales - tot_exp
    total_stock_items = df_p['quantity'].sum() if not df_p.empty else 0
    total_debts = df_d['remaining'].sum() if not df_d.empty else 0.0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 إجمالي المبيعات", f"{tot_sales:,.1f} د.ك")
    c2.metric("💸 إجمالي المصروفات", f"{tot_exp:,.1f} د.ك")
    c3.metric("📈 صافي العائد", f"{net_profit:,.1f} د.ك")
    c4.metric("⚠️ ديون العملاء المتبقية", f"{total_debts:,.1f} د.ك")
    
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🏆 مبيعات الموظفين مرئياً")
        if not df_s.empty and 'employee_name' in df_s.columns:
            emp_chart_data = df_s.groupby('employee_name')['price'].sum()
            st.bar_chart(emp_chart_data)
        else:
            st.info("لا توجد بيانات مبيعات كافية للرسم البياني.")
            
    with col_chart2:
        st.markdown("### 📦 حركة المبيعات حسب المنتجات")
        if not df_s.empty:
            prod_chart_data = df_s.groupby('product_name')['quantity_sold'].sum()
            st.bar_chart(prod_chart_data)
        else:
            st.info("لا توجد منتجات مباعة حتى الآن.")

# ----------------- تبويب 1: المخزون -----------------
with tab1:
    st.subheader("📦 إدارة المخزون والفئات المنظمة")
    
    with st.expander("➕ إضافة منتج جديد للفئات المنظمة"):
        with st.form("add_prod", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                category = st.selectbox("الفئة الرئيسية:", main_categories)
                name = st.text_input("اسم المنتج التفصيلي:")
            with col2:
                color = st.text_input("اللون:")
                dims = st.text_input("المقاسات:")
            with col3:
                price = st.number_input("السعر:", value=0.0)
                quantity = st.number_input("العدد المتوفر:", value=0, step=1)
                location = st.selectbox("الفرع:", ["سوق المروة", "السوق الصيني"])
            
            if st.form_submit_button("حفظ المنتج بالقسم"):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO products_catalog (category, name, color, dims, price, quantity, location) VALUES (?,?,?,?,?,?,?)", 
                             (category, name, color, dims, price, quantity, location))
                conn.commit()
                conn.close()
                st.success(f"✅ تم حفظ المنتج في فئة ({category}) بنجاح!")
                st.rerun()

    with st.expander("✏️ تعديل أو حذف منتج موجود"):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        all_products_db = cursor.execute("SELECT * FROM products_catalog").fetchall()
        
        if all_products_db:
            prod_names = [p['name'] for p in all_products_db]
            selected_prod_name = st.selectbox("اختر المنتج للتعامل معه:", prod_names)
            
            product = cursor.execute("SELECT * FROM products_catalog WHERE name = ?", (selected_prod_name,)).fetchone()
            
            if product:
                st.info(f"المنتج المحدد: {product['name']} (الفئة: {product['category']}) | الكمية الحالية: {product['quantity']}")
                with st.form("edit_delete_prod"):
                    new_category = st.selectbox("تعديل الفئة:", main_categories, index=main_categories.index(product['category']) if product['category'] in main_categories else 0)
                    new_price = st.number_input("تعديل السعر:", value=float(product["price"] if product["price"] is not None else 0.0))
                    new_qty = st.number_input("تعديل الكمية:", value=int(product["quantity"] if product["quantity"] is not None else 0), step=1)
                    new_dims = st.text_input("تعديل المقاسات:", value=str(product["dims"] if product["dims"] is not None else ""))
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        update_submitted = st.form_submit_button("حفظ التعديلات")
                    with col_btn2:
                        delete_submitted = st.form_submit_button("🗑️ حذف المنتج نهائياً")
                    
                    if update_submitted:
                        cursor.execute("UPDATE products_catalog SET category=?, price=?, quantity=?, dims=? WHERE id=?", (new_category, new_price, new_qty, new_dims, product['id']))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم تحديث بيانات المنتج بنجاح!")
                        st.rerun()
                    
                    if delete_submitted:
                        cursor.execute("DELETE FROM products_catalog WHERE id=?", (product['id'],))
                        conn.commit()
                        conn.close()
                        st.warning("🗑️ تم حذف المنتج من النظام نهائياً!")
                        st.rerun()
        else:
            st.info("لا توجد منتجات مسجلة لتعديلها.")
        conn.close()

    st.divider()
    
    conn = sqlite3.connect(DB_PATH)
    all_data = pd.read_sql("SELECT id AS 'رقم الـ ID', category AS 'الفئة', name AS 'المنتج', color AS 'اللون', dims AS 'المقاسات', price AS 'السعر', quantity AS 'الكمية', location AS 'الفرع' FROM products_catalog", conn)
    conn.close()

    if not all_data.empty:
        selected_cat = st.selectbox("🔍 تصفية الجدول حسب الفئة:", ["الكل (عرض كل الفئات)"] + list(all_data['الفئة'].dropna().unique()))
        
        if selected_cat != "الكل (عرض كل الفئات)":
            df_filtered = all_data[all_data['الفئة'] == selected_cat]
        else:
            df_filtered = all_data
            
        st.dataframe(df_filtered, use_container_width=True)
        
        if (all_data['الكمية'] < 5).any():
            st.warning("⚠️ تنبيه: هناك منتجات اقتربت من النفاذ (أقل من 5 قطع)!")
    else:
        st.info("لم يتم تسجيل أي منتجات حتى الآن.")

# ----------------- تبويب 2: العملاء -----------------
with tab2:
    st.subheader("👥 بنك العملاء")
    with st.form("add_client", clear_on_submit=True):
        c_name = st.text_input("اسم العميل:")
        c_phone = st.text_input("رقم الهاتف:")
        c_interest = st.text_input("المنتج المهتم به:")
        c_notes = st.text_input("ملاحظات إضافية:")
        if st.form_submit_button("حفظ العميل في البنك"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO clients (name, phone, interest, notes) VALUES (?,?,?,?)", (c_name, c_phone, c_interest, c_notes))
            conn.commit()
            conn.close()
            st.success("✅ تم حفظ العميل بنجاح!")
            st.rerun()
            
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT id AS 'م', name AS 'اسم العميل', phone AS 'الهاتف', interest AS 'الاهتمام', notes AS 'ملاحظات' FROM clients", conn), use_container_width=True)
    conn.close()

# ----------------- تبويب 3: الصفقات -----------------
with tab3:
    st.subheader("📈 تسجيل صفقة بيع (وتخصيم المخزون أوتوماتيك)")
    
    conn = sqlite3.connect(DB_PATH)
    products_list = pd.read_sql("SELECT id, name, quantity, price FROM products_catalog WHERE quantity > 0", conn)
    emps_list = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
    conn.close()

    if not emps_list:
        st.warning("⚠️ تنبيه: يرجى إضافة موظفين أولاً من تبويب 'أداء الموظفين' حتى تتمكن من اختيار الموظف المسؤول عن الصفقة.")

    if not products_list.empty:
        with st.form("make_sale", clear_on_submit=True):
            client_sale_name = st.text_input("اسم العميل المشتري:")
            selected_emp = st.selectbox("الموظف المسؤول عن البيع:", emps_list if emps_list else ["غير محدد"])
            selected_prod_name = st.selectbox("اختر المنتج المباع:", products_list['name'].tolist())
            sold_qty = st.number_input("الكمية المباعة:", min_value=1, value=1, step=1)
            
            if st.form_submit_button("إتمام البيع وتسجيل الصفقة"):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                prod_info = cursor.execute("SELECT id, quantity, price FROM products_catalog WHERE name = ?", (selected_prod_name,)).fetchone()
                
                if prod_info:
                    p_id, current_qty, p_price = prod_info[0], prod_info[1], prod_info[2]
                    if sold_qty > current_qty:
                        st.error(f"⚠️ الكمية غير متوفرة! المتبقي: {current_qty}")
                    else:
                        new_remaining_qty = current_qty - sold_qty
                        total_sale_price = p_price * sold_qty
                        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                        
                        cursor.execute("UPDATE products_catalog SET quantity = ? WHERE id = ?", (new_remaining_qty, p_id))
                        cursor.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name) VALUES (?,?,?,?,?,?)", 
                                       (client_sale_name, selected_prod_name, total_sale_price, sold_qty, sale_date, selected_emp))
                        
                        conn.commit()
                        conn.close()
                        st.success(f"🎉 تم البيع بنجاح بواسطة الموظف ({selected_emp})! تم خصم {sold_qty} من {selected_prod_name}.")
                        st.rerun()
                conn.close()
    else:
        st.info("لا توجد منتجات متوفرة حالياً للبيع.")

    st.divider()
    st.markdown("### سجل الصفقات السابقة:")
    conn = sqlite3.connect(DB_PATH)
    df_sales = pd.read_sql("SELECT id AS 'رقم الصفقة', client_name AS 'اسم العميل', employee_name AS 'الموظف المسؤول', product_name AS 'المنتج', price AS 'الإجمالي', quantity_sold AS 'الكمية', date AS 'التاريخ والوقت' FROM sales", conn)
    conn.close()
    st.dataframe(df_sales, use_container_width=True)

# ----------------- تبويب 4: التقارير المالية -----------------
with tab4:
    st.subheader("📊 التقارير المالية الصافية وتصدير البيانات")
    conn = sqlite3.connect(DB_PATH)
    df_sales_rep = pd.read_sql("SELECT * FROM sales", conn)
    total_sales = df_sales_rep['price'].sum() if not df_sales_rep.empty else 0.0
    
    df_exp_rep = pd.read_sql("SELECT * FROM expenses", conn)
    total_expenses = df_exp_rep['amount'].sum() if not df_exp_rep.empty else 0.0
    
    df_debts_rep = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المبيعات", f"{total_sales} د.ك")
    col2.metric("إجمالي المصروفات", f"{total_expenses} د.ك")
    col3.metric("صافي الربح", f"{total_sales - total_expenses} د.ك")
    
    if not df_sales_rep.empty:
        st.write("### أكثر المنتجات مبيعاً")
        st.bar_chart(df_sales_rep.groupby('product_name')['quantity_sold'].sum())
        
    st.divider()
    st.markdown("<h3 style='direction: rtl;'>📥 تصدير تقارير وشيست الشغل (ملفات CSV جاهزة)</h3>", unsafe_allow_html=True)
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        if not df_sales_rep.empty:
            csv_sales = df_sales_rep.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل تقرير المبيعات", csv_sales, "sales_report.csv", "text/csv")
        else:
            st.info("لا توجد مبيعات للتصدير.")
            
    with col_exp2:
        if not df_exp_rep.empty:
            csv_exp = df_exp_rep.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل تقرير المصروفات", csv_exp, "expenses_report.csv", "text/csv")
        else:
            st.info("لا توجد مصروفات للتصدير.")
            
    with col_exp3:
        if not df_debts_rep.empty:
            csv_debts = df_debts_rep.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل تقرير الآجل والحسابات", csv_debts, "debts_report.csv", "text/csv")
        else:
            st.info("لا توجد ديون للتصدير.")

# ----------------- تبويب 5: دفتر الآجل -----------------
with tab5:
    st.subheader("💰 دفتر الحسابات والآجل ومتابعة التحصيل")
    
    with st.expander("➕ تسجيل عملية آجل أو عربون جديدة"):
        with st.form("add_debt", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            d_name = col1.text_input("اسم العميل:")
            d_phone = col1.text_input("رقم هاتف العميل:")
            d_total = col2.number_input("إجمالي المبلغ:", value=0.0)
            d_paid = col3.number_input("المبلغ المدفوع (العربون):", value=0.0)
            
            if st.form_submit_button("حفظ الحساب"):
                remaining = d_total - d_paid
                status = "خالص" if remaining <= 0 else "متبقي"
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO debts (client_name, phone, total_amount, paid_amount, remaining, status) VALUES (?,?,?,?,?,?)",
                             (d_name, d_phone, d_total, d_paid, remaining, status))
                conn.commit()
                conn.close()
                st.success("✅ تم تسجيل الحساب بنجاح!")
                st.rerun()
                
    with st.expander("💸 تسجيل دفعة سداد جديدة لعميل"):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        debts_list = conn.execute("SELECT * FROM debts WHERE status = 'متبقي'").fetchall()
        
        if debts_list:
            debt_options = {f"سجل رقم ({d['id']}) - العميل: {d['client_name']} (المتبقي عليه: {d['remaining']} د.ك)": d['id'] for d in debts_list}
            selected_debt_label = st.selectbox("اختر الحساب المراد السداد فيه:", list(debt_options.keys()))
            chosen_debt_id = debt_options[selected_debt_label]
            
            with st.form("pay_form"):
                extra_pay = st.number_input("قيمة الدفعة الجديدة:", value=0.0, min_value=0.0)
                if st.form_submit_button("تحديث وإضافة الدفعة"):
                    curr_data = conn.execute("SELECT total_amount, paid_amount FROM debts WHERE id=?", (chosen_debt_id,)).fetchone()
                    if curr_data:
                        new_paid_total = curr_data['paid_amount'] + extra_pay
                        new_remaining = curr_data['total_amount'] - new_paid_total
                        new_status = "خالص" if new_remaining <= 0 else "متبقي"
                        
                        conn.execute("UPDATE debts SET paid_amount=?, remaining=?, status=? WHERE id=?", 
                                   (new_paid_total, new_remaining, new_status, chosen_debt_id))
                        conn.commit()
                        st.success("✅ تم تحديث السداد بنجاح!")
                        st.rerun()
        else:
            st.info("لا توجد حسابات متبقية أو ديون مستحقة حالياً.")
        conn.close()

    st.divider()
    st.markdown("### ⚠️ قائمة العملاء الذين عليهم مبالغ متبقية للمتابعة:")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    active_debts = conn.execute("SELECT * FROM debts WHERE status = 'متبقي'").fetchall()
    conn.close()

    if active_debts:
        for d in active_debts:
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.error(f"👤 {d['client_name']} | المتبقي: **{d['remaining']} د.ك**")
            c2.text(f"📞 {d['phone'] if d['phone'] else 'لا يوجد رقم'}")
            
            if c3.button(f"✏️ تعديل", key=f"edit_{d['id']}"):
                st.session_state[f"editing_{d['id']}"] = True
            
            if st.session_state.get(f"editing_{d['id']}"):
                with st.form(f"form_edit_{d['id']}"):
                    new_phone = st.text_input("رقم الهاتف الجديد:", value=d['phone'] if d['phone'] else "")
                    if st.form_submit_button("حفظ التعديل"):
                        conn_edit = sqlite3.connect(DB_PATH)
                        conn_edit.execute("UPDATE debts SET phone=? WHERE id=?", (new_phone, d['id']))
                        conn_edit.commit()
                        conn_edit.close()
                        st.session_state[f"editing_{d['id']}"] = False
                        st.success("✅ تم التحديث!")
                        st.rerun()
            
            if d['phone']:
                wa_msg = f"السلام عليكم يا فندم، تذكرة من سوق المروة للأثاث والديكور بخصوص المبلغ المتبقي وقدره {d['remaining']} د.ك. وشكراً لتعاملكم معنا."
                c4.markdown(f'<a href="https://wa.me/{d["phone"]}?text={wa_msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">💬 واتساب</button></a>', unsafe_allow_html=True)
            else:
                c4.text("⚠️ أضف رقم")
    else:
        st.success("🎉 ممتاز! لا توجد أي مبالغ متأخرة على العملاء حالياً.")

# ----------------- تبويب 6: المصروفات -----------------
with tab6:
    st.subheader("💸 إدارة المصروفات اليومية")
    with st.form("add_expense", clear_on_submit=True):
        col1, col2 = st.columns(2)
        reason = col1.text_input("سبب المصروف (نقل، خامات، أجرة..):")
        amount = col2.number_input("قيمة المبلغ:", value=0.0)
        if st.form_submit_button("تسجيل المصروف"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (reason, amount, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("✅ تم تسجيل المصروف!")
            st.rerun()
            
    conn = sqlite3.connect(DB_PATH)
    df_exp = pd.read_sql("SELECT id AS 'رقم السجل', reason AS 'سبب المصروف', amount AS 'المبلغ', date AS 'التاريخ' FROM expenses", conn)
    st.dataframe(df_exp, use_container_width=True)
    conn.close()

# ----------------- تبويب 7: الفواتير -----------------
with tab7:
    st.subheader("🧾 إصدار وعرض فاتورة / إيصال عميل")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    debts_for_invoice = conn.execute("SELECT * FROM debts").fetchall()
    conn.close()
    
    if debts_for_invoice:
        inv_options = {f"فاتورة للعميل: {d['client_name']} (الإجمالي: {d['total_amount']} | المتبقي: {d['remaining']})": d for d in debts_for_invoice}
        selected_inv_label = st.selectbox("اختر العميل لطباعة / عرض الفاتورة:", list(inv_options.keys()))
        chosen_inv = inv_options[selected_inv_label]
        
        st.markdown("---")
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f9f9f9; color: #000;">
            <h2 style="text-align: center; color: #2E7D32;">🛒 سوق المروة للأثاث والديكور</h2>
            <hr>
            <p><b>رقم الإيصال:</b> #{chosen_inv['id']}</p>
            <p><b>اسم العميل:</b> {chosen_inv['client_name']}</p>
            <p><b>إجمالي المبلغ المطلوب:</b> {chosen_inv['total_amount']} د.ك</p>
            <p><b>المبلغ المدفوع (العربون):</b> {chosen_inv['paid_amount']} د.ك</p>
            <p><b>المبلغ المتبقي:</b> <span style="color: red; font-weight: bold;">{chosen_inv['remaining']} د.ك</span></p>
            <p><b>حالة الحساب:</b> <span style="color: {'green' if chosen_inv['status']=='خالص' else 'orange'}; font-weight: bold;">{chosen_inv['status']}</span></p>
            <hr>
            <p style="text-align: center; font-size: 14px; color: #555;">شكراً لتعاملكم معنا - نسعى دائماً لخدمتكم بأفضل جودة</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("لا توجد حسابات أو فواتير مسجلة لإصدار إيصال لها.")

# ----------------- تبويب 8: مشاريع التنفيذ -----------------
with tab8:
    st.subheader("🏗️ إدارة مشاريع التنفيذ وأرشفة الصور (قبل وبعد)")
    
    with st.expander("➕ إضافة مشروع تشطيب/دهانات جديد مع أرشفة الصور"):
        with st.form("add_proj", clear_on_submit=True):
            col1, col2 = st.columns(2)
            p_name = col1.text_input("اسم المشروع/الموقع:")
            c_name = col1.text_input("اسم العميل:")
            status = col2.selectbox("المرحلة الحالية:", ["تأسيس", "معجون", "دهان أولي", "تشطيب نهائي", "تسليم"])
            total_cost = col2.number_input("القيمة الإجمالية للمشروع:", value=0.0)
            paid_cost = col2.number_input("المبلغ المحصل:", value=0.0)
            notes = st.text_area("ملاحظات (الخامات المطلوبة / متطلبات العميل):")
            
            b_img = st.file_uploader("📸 صورة الموقع (قبل التنفيذ):", type=['jpg', 'jpeg', 'png'])
            a_img = st.file_uploader("✨ صورة الموقع (بعد التشطيب):", type=['jpg', 'jpeg', 'png'])
            
            if st.form_submit_button("حفظ المشروع بالصور وأرشفته"):
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
                st.success("✅ تم حفظ المشروع وأرشفة الصور بنجاح!")
                st.rerun()

    st.divider()
    st.markdown("### 📂 معرض أعمال ومشاريع سوق المروة (قبل وبعد):")
    conn = sqlite3.connect(DB_PATH)
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    
    if projects:
        for p in projects:
            with st.container(border=True):
                st.markdown(f"### 📍 المشروع: {p[1]} | العميل: {p[2]}")
                c1, c2 = st.columns(2)
                if len(p) > 7 and p[7]:
                    c1.image(p[7], caption="حالة الموقع (قبل)", use_container_width=True)
                else:
                    c1.info("لا توجد صورة قبل")
                    
                if len(p) > 8 and p[8]:
                    c2.image(p[8], caption="النتيجة النهائية (بعد)", use_container_width=True)
                else:
                    c2.info("لا توجد صورة بعد")
                    
                st.write(f"**المرحلة:** {p[3]} | **الإجمالي:** {p[4]} د.ك | **المحصل:** {p[5]} د.ك")
                if p[6]:
                    st.text(f"ملاحظات: {p[6]}")
                
                with st.expander(f"💸 تسجيل مصروف خاص للمشروع: {p[1]}"):
                    with st.form(f"exp_{p[0]}"):
                        e_reason = st.text_input("سبب المصروف:")
                        e_amount = st.number_input("القيمة:")
                        if st.form_submit_button("حفظ مصروف المشروع"):
                            if e_reason.strip() and e_amount > 0:
                                conn = sqlite3.connect(DB_PATH)
                                conn.execute("INSERT INTO expenses (reason, amount, date) VALUES (?,?,?)", (f"مشروع {p[1]}: {e_reason}", e_amount, datetime.now().strftime("%Y-%m-%d")))
                                conn.commit()
                                conn.close()
                                st.success("✅ تم تسجيل المصروف وإضافته لدفتر المصروفات العام بنجاح!")
                                st.rerun()
                            else:
                                st.error("⚠️ يرجى إدخال سبب المصروف والقيمة بشكل صحيح.")
    else:
        st.info("لا توجد مشاريع مسجلة حتى الآن.")

    st.divider()
    st.markdown("### 🏗️ إدارة المصروفات وأجور العمال المرتبطة بالمشاريع")
    
    conn_p_ext = sqlite3.connect(DB_PATH)
    active_projects = conn_p_ext.execute("SELECT id, project_name, client_name FROM projects").fetchall()
    conn_p_ext.close()

    if active_projects:
        with st.expander("📂 افتح لوحة إدارة مصروفات وأجور مشاريع التنفيذ"):
            proj_map = {f"مشروع: {p[1]} (العميل: {p[2]}) [رقم {p[0]}]": p[0] for p in active_projects}
            selected_proj_str = st.selectbox("اختر المشروع المطلوب:", list(proj_map.keys()), key="exp_proj_select")
            chosen_proj_id = proj_map[selected_proj_str]
            
            with st.form("project_expense_worker_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    exp_type = st.selectbox("نوع البند:", ["أجور عمالة يومية", "خامات ومواد إضافية", "نقليات ومواصلات", "مصروفات متنوعة أخرى"])
                with col2:
                    exp_cost = st.number_input("القيمة (د.ك):", min_value=0.0, value=0.0, step=5.0)
                
                exp_details = st.text_input("التفاصيل (مثل: اسم العامل، عدد ساعات العمل، أو نوع الخامة المشتراة):")
                
                submitted_exp = st.form_submit_button("💾 حفظ وتسجيل المصروف للمشروع")
                
                if submitted_exp:
                    if exp_details.strip() != "":
                        conn_name = sqlite3.connect(DB_PATH)
                        p_name_res = conn_name.execute("SELECT project_name FROM projects WHERE id = ?", (chosen_proj_id,)).fetchone()
                        conn_name.close()
                        
                        target_p_name = p_name_res[0] if p_name_res else "مفهرس"
                        formatted_reason = f"مشروع [{target_p_name}] - {exp_type}: {exp_details}"
                        
                        conn_save = sqlite3.connect(DB_PATH)
                        conn_save.execute("INSERT INTO expenses (reason, amount, date) VALUES (?, ?, ?)", 
                                          (formatted_reason, exp_cost, datetime.now().strftime("%Y-%m-%d")))
                        conn_save.commit()
                        conn_save.close()
                        
                        st.success(f"✅ تم حفظ بند المصروف ({exp_cost} د.ك) بنجاح وإضافته إلى دفتر المصروفات والربح العام للمتجر!")
                        st.rerun()
                    else:
                        st.error("⚠️ يرجى كتابة تفاصيل صحيحة للبند أو المصروف.")
    else:
        st.info("ℹ️ لا توجد مشاريع مسجلة حالياً لتسجيل مصروفات أو أجور عمالة لها.")

# ----------------- تبويب 9: أداء الموظفين -----------------
with tab9:
    st.subheader("🏅 تقييم وأداء فريق العمل داخل سوق المروة")
    with st.expander("➕ إضافة موظف جديد لسوق المروة"):
        with st.form("add_emp_form", clear_on_submit=True):
            emp_name_input = st.text_input("اسم الموظف الثلاثي:")
            if st.form_submit_button("حفظ الموظف"):
                if emp_name_input.strip() != "":
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO employees (name) VALUES (?)", (emp_name_input.strip(),))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ تم إضافة الموظف ({emp_name_input}) بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ يرجى كتابة اسم الموظف بشكل صحيح.")

    st.divider()
    conn = sqlite3.connect(DB_PATH)
    sales_check = pd.read_sql("SELECT * FROM sales", conn)
    employees_check = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()
    
    if not employees_check.empty:
        st.dataframe(employees_check.rename(columns={'id': 'رقم الموظف', 'name': 'اسم الموظف'}), use_container_width=True)
        if not sales_check.empty and 'employee_name' in sales_check.columns:
            st.markdown("#### إحصائيات المبيعات مسجلة بأسماء الموظفين:")
            emp_summary = sales_check.groupby('employee_name').agg(
                عدد_الصفقات=('id', 'count'),
                إجمالي_المبيعات_دك=('price', 'sum')
            ).reset_index().rename(columns={'employee_name': 'اسم الموظف', 'عدد_الصفقات': 'عدد الصفقات المباعة', 'إجمالي_المبيعات_دك': 'إجمالي المبيعات (د.ك)'})
            st.dataframe(emp_summary, use_container_width=True)
        else:
            st.info("لم يتم تسجيل صفقات مرتبطة بالموظفين حتى الآن.")
    else:
        st.info("لا يوجد موظفون مسجلون حالياً.")