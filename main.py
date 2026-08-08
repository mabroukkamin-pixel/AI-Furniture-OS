import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "sovereign_100_matrix.db"
UPLOAD_FOLDER = "project_assets"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. المخزون
    c.execute('''CREATE TABLE IF NOT EXISTS products_catalog 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, barcode TEXT, image_path TEXT)''')
    
    # 2. العملاء (CRM)
    c.execute('''CREATE TABLE IF NOT EXISTS clients 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, interest TEXT, notes TEXT)''')
                 
    # 3. المبيعات والصفقات
    c.execute('''CREATE TABLE IF NOT EXISTS sales 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT, payment_method TEXT, branch TEXT, status TEXT, cancel_reason TEXT)''')
        
    # 4. دفتر الديون والآجل وعربون العملاء
    c.execute('''CREATE TABLE IF NOT EXISTS debts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, phone TEXT, total_amount REAL, paid_amount REAL, remaining REAL, status TEXT, due_date TEXT)''')
        
    # 5. المصروفات
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, date TEXT, category TEXT, payment_method TEXT, receipt_img TEXT)''')
        
    # 6. المشاريع والتشطيبات
    c.execute('''CREATE TABLE IF NOT EXISTS projects 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT, total_cost REAL, paid_cost REAL, notes TEXT, before_img TEXT, after_img TEXT, team TEXT, deadline TEXT, contract_file TEXT)''')
        
    # 7. الموظفين وشؤون العاملين (الأقسام الكاملة)
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT, hire_date TEXT, role TEXT, salary REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employee_attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, date TEXT, status TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employee_bonuses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, amount REAL, reason TEXT, date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employee_notes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, note TEXT, date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employee_shifts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, shift_type TEXT, date TEXT)''')

    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

main_categories = [
    "أثاث التخزين (كبتات وخزانات)",
    "أثاث الجلوس (كنب وكراسي)",
    "الطاولات والمكاتب",
    "استاندات وعرض",
    "ديكور وإضاءة",
    "مفروشات ونوم",
    "منوعات ومواسم"
]

# ==========================================
# 📱 القائمة الجانبية (Sidebar Navigation)
# ==========================================
with st.sidebar:
    st.title("🛒 سوق المروة للأثاث")
    st.divider()
    
    current_page = st.radio(
        "القائمة الرئيسية:",
        [
            "📊 المؤشرات",
            "📦 المخزون",
            "👥 العملاء",
            "📈 الصفقات",
            "📊 التقارير",
            "💰 دفتر الآجل والديون",
            "💸 المصروفات",
            "🧾 الفواتير",
            "🏗️ المشاريع",
            "🏅 الموظفين"
        ]
    )
    
    st.divider()
    st.subheader("📱 واجهة الميدان السريعة")
    dark_mode_toggle = st.toggle("🌙 وضع الظلام (Dark Mode)")
    if dark_mode_toggle:
        st.markdown("<style>body { background-color: #0e1117; color: #ffffff; }</style>", unsafe_allow_html=True)

    mobile_action = st.radio("اختر العملية السريعة:", ["لا شيء", "تسجيل صفقة", "تسجيل مصروف", "مشاركة يومية عبر واتساب"])
    
    if mobile_action == "تسجيل مصروف":
        with st.form("mobile_expense_form", clear_on_submit=True):
            m_reason = st.text_input("بيان المصروف:")
            m_amount = st.number_input("القيمة:", value=0.0, min_value=0.0)
            if st.form_submit_button("حفظ سريع"):
                if m_reason.strip() and m_amount > 0:
                    conn_m = sqlite3.connect(DB_PATH)
                    conn_m.execute("INSERT INTO expenses (reason, amount, date, category, payment_method) VALUES (?,?,?,?,?)", 
                                   (f"[ميداني] {m_reason}", m_amount, datetime.now().strftime("%Y-%m-%d"), "نثريات", "كاش"))
                    conn_m.commit()
                    conn_m.close()
                    st.success("✅ تم حفظ المصروف ميدانياً!")
                    st.rerun()
                else:
                    st.error("⚠️ أدخل البيانات بشكل صحيح.")
    
    elif mobile_action == "تسجيل صفقة":
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
                
                if st.form_submit_button("إتمام البيع الميداني"):
                    conn_m2 = sqlite3.connect(DB_PATH)
                    cur_m = conn_m2.cursor()
                    p_row = cur_m.execute("SELECT id, quantity, price FROM products_catalog WHERE name = ?", (m_prod,)).fetchone()
                    if p_row and m_qty <= p_row[1]:
                        new_q = p_row[1] - m_qty
                        tot_p = p_row[2] * m_qty
                        cur_m.execute("UPDATE products_catalog SET quantity = ? WHERE id = ?", (new_q, p_row[0]))
                        cur_m.execute("INSERT INTO sales (client_name, product_name, price, quantity_sold, date, employee_name, payment_method, branch, status, cancel_reason) VALUES (?,?,?,?,?,?,?,?,?,?)", 
                                      (m_client if m_client else "عميل ميداني", m_prod, tot_p, m_qty, datetime.now().strftime("%Y-%m-%d %H:%M"), m_emp, "كاش", "سوق المروة", "مكتملة", ""))
                        conn_m2.commit()
                        conn_m2.close()
                        st.success("🎉 تم إتمام الصفقة الميدانية!")
                        st.rerun()
                    else:
                        st.error("⚠️ الكمية المطلوبة غير متوفرة بالمخزون.")
                        conn_m2.close()
        else:
            st.warning("⚠️ يرجى التأكد من توفر منتجات وموظفين مسجلين أولاً.")
    
    elif mobile_action == "مشاركة يومية عبر واتساب":
        conn_m = sqlite3.connect(DB_PATH)
        df_s_mob = pd.read_sql("SELECT price FROM sales WHERE date LIKE ?", conn_m, params=(datetime.now().strftime("%Y-%m-%d") + "%",))
        conn_m.close()
        day_total = df_s_mob['price'].sum() if not df_s_mob.empty else 0.0
        wa_text = f"ملخص مبيعات اليوم ({datetime.now().strftime('%Y-%m-%d')}): {day_total} د.ك - سوق المروة للأثاث والديكور"
        st.markdown(f'<a href="https://api.whatsapp.com/send?text={wa_text}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; width:100%;">📤 مشاركة ملخص اليوم عبر واتساب</button></a>', unsafe_allow_html=True)

st.title(f"{current_page}")
st.divider()

# ----------------- 1. المؤشرات -----------------
if current_page == "📊 المؤشرات":
    st.subheader("📊 لوحة المؤشرات والتحليلات المرئية المتقدمة")
    conn = sqlite3.connect(DB_PATH)
    df_s = pd.read_sql("SELECT * FROM sales", conn)
    df_e = pd.read_sql("SELECT * FROM expenses", conn)
    df_d = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    
    tot_sales = df_s[df_s['status'] != 'ملغاة']['price'].sum() if not df_s.empty else 0.0
    tot_exp = df_e['amount'].sum() if not df_e.empty else 0.0
    net_profit = tot_sales - tot_exp
    total_debts = df_d['remaining'].sum() if not df_d.empty else 0.0
    
    c1, c2 = st.columns(2)
    c1.metric("💰 إجمالي المبيعات", f"{tot_sales:,.1f} د.ك")
    c2.metric("💸 إجمالي المصروفات", f"{tot_exp:,.1f} د.ك")
    c3, c4 = st.columns(2)
    c3.metric("📈 صافي العائد والأرباح", f"{net_profit:,.1f} د.ك")
    c4.metric("⚠️ إجمالي الديون المستحقة", f"{total_debts:,.1f} د.ك")

# ----------------- 2. المخزون -----------------
elif current_page == "📦 المخزون":
    st.subheader("📦 إدارة المخزون والفئات المنظمة للمنتجات")
    
    # الجدول الشامل في الصدارة مع التصفية حسب الفئة
    conn = sqlite3.connect(DB_PATH)
    df_all_prod = pd.read_sql("SELECT id AS 'رقم ID', category AS 'الفئة', name AS 'المنتج', color AS 'اللون', dims AS 'المقاسات', price AS 'السعر', quantity AS 'الكمية', location AS 'الفرع', barcode AS 'الباركود' FROM products_catalog", conn)
    conn.close()

    st.markdown("### 📋 جدول استعراض وتصفية المنتجات بالمخزون")
    selected_filter_cat = st.selectbox("🔍 تصفية الجدول حسب الفئة:", ["الكل (عرض كل الفئات)"] + main_categories)
    
    if selected_filter_cat != "الكل (عرض كل الفئات)":
        filtered_df = df_all_prod[df_all_prod['الفئة'] == selected_filter_cat]
    else:
        filtered_df = df_all_prod
        
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()

    search_barcode_input = st.text_input("🔍 مسح كود الباركود بالكاميرا أو إدخاله للبحث الفوري:")
    if search_barcode_input:
        conn = sqlite3.connect(DB_PATH)
        res_bc = conn.execute("SELECT * FROM products_catalog WHERE barcode = ?", (search_barcode_input,)).fetchone()
        conn.close()
        if res_bc:
            st.success(f"✅ تم العثور على الصنف: {res_bc[2]} | السعر: {res_bc[5]} د.ك | الكمية: {res_bc[6]} | الفرع: {res_bc[7]}")
            if res_bc[9] and os.path.exists(res_bc[9]):
                st.image(res_bc[9], width=200)
        else:
            st.warning("⚠️ لا يوجد صنف مسجل بهذا الباركود.")

    conn = sqlite3.connect(DB_PATH)
    low_stock_df = pd.read_sql("SELECT name AS 'المنتج', quantity AS 'الكمية المتبقية', location AS 'الفرع' FROM products_catalog WHERE quantity <= 3", conn)
    conn.close()
    if not low_stock_df.empty:
        st.error("🚨 تنبيه انخفاض المخزون (Low Stock Alerts): الأصناف التالية اقتربت على النفاد:")
        st.dataframe(low_stock_df, use_container_width=True)

    with st.expander("➕ إضافة منتج جديد (مع إرفاق الصور والباركود)"):
        with st.form("add_prod", clear_on_submit=True):
            category = st.selectbox("الفئة الرئيسية:", main_categories)
            name = st.text_input("اسم المنتج التفصيلي:")
            color = st.text_input("اللون:")
            dims = st.text_input("المقاسات:")
            price = st.number_input("السعر:", value=0.0, min_value=0.0)
            quantity = st.number_input("العدد المتوفر:", value=0, step=1, min_value=0)
            location = st.selectbox("الفرع:", ["سوق المروة", "السوق الصيني"])
            barcode = st.text_input("كود الباركود:")
            p_img = st.file_uploader("إرفاق صورة المنتج:", type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("حفظ المنتج بالكامل"):
                img_path = None
                if p_img:
                    img_path = os.path.join(UPLOAD_FOLDER, f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
                    with open(img_path, "wb") as f:
                        f.write(p_img.getbuffer())

                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO products_catalog (category, name, color, dims, price, quantity, location, barcode, image_path) VALUES (?,?,?,?,?,?,?,?,?)", 
                           (category, name, color, dims, price, quantity, location, barcode, img_path))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ المنتج وإرفاق الصورة بنجاح!")
                st.rerun()

    st.markdown("### ⚙️ تعديل أو حذف منتج من المخزون")
    conn = sqlite3.connect(DB_PATH)
    df_products_edit = pd.read_sql("SELECT id, category, name, color, dims, price, quantity, location, barcode FROM products_catalog", conn)
    conn.close()

    if not df_products_edit.empty:
        prod_options_dict = {f"{row['name']} (الفئة: {row['category']} - الكمية: {row['quantity']})": row['id'] for _, row in df_products_edit.iterrows()}
        selected_prod_key = st.selectbox("اختر المنتج لتعديله أو حذفه:", list(prod_options_dict.keys()))
        selected_prod_id = prod_options_dict[selected_prod_key]
        
        p_row = df_products_edit[df_products_edit['id'] == selected_prod_id].iloc[0]

        with st.form("edit_product_form"):
            e_cat = st.selectbox("تعديل الفئة:", main_categories, index=main_categories.index(p_row['category']) if p_row['category'] in main_categories else 0)
            e_name = st.text_input("تعديل اسم المنتج:", value=str(p_row['name']))
            e_color = st.text_input("تعديل اللون:", value=str(p_row['color']) if pd.notna(p_row['color']) else "")
            e_dims = st.text_input("تعديل المقاسات:", value=str(p_row['dims']) if pd.notna(p_row['dims']) else "")
            e_price = st.number_input("تعديل السعر:", value=float(p_row['price']) if pd.notna(p_row['price']) else 0.0, min_value=0.0)
            e_qty = st.number_input("تعديل الكمية:", value=int(p_row['quantity']) if pd.notna(p_row['quantity']) else 0, min_value=0, step=1)
            e_loc = st.selectbox("تعديل الفرع:", ["سوق المروة", "السوق الصيني"], index=0 if p_row['location'] == "سوق المروة" else 1)
            e_bc = st.text_input("تعديل الباركود:", value=str(p_row['barcode']) if pd.notna(p_row['barcode']) else "")

            c_btn1, c_btn2 = st.columns(2)
            update_btn = c_btn1.form_submit_button("💾 حفظ التعديلات")
            delete_btn = c_btn2.form_submit_button("🗑️ حذف المنتج نهائياً")

            if update_btn:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("UPDATE products_catalog SET category = ?, name = ?, color = ?, dims = ?, price = ?, quantity = ?, location = ?, barcode = ? WHERE id = ?",
                           (e_cat, e_name, e_color, e_dims, e_price, e_qty, e_loc, e_bc, selected_prod_id))
                conn.commit()
                conn.close()
                st.success("✅ تم تحديث بيانات المنتج بنجاح!")
                st.rerun()

            if delete_btn:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("DELETE FROM products_catalog WHERE id = ?", (selected_prod_id,))
                conn.commit()
                conn.close()
                st.warning("⚠️ تم حذف المنتج بنجاح!")
                st.rerun()

# ----------------- 3. العملاء (CRM) -----------------
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
    st.dataframe(pd.read_sql("SELECT name AS 'اسم العميل', phone AS 'الهاتف', interest AS 'الاهتمامات', notes AS 'ملاحظات' FROM clients", conn), use_container_width=True)
    conn.close()

# ----------------- 4. الصفقات والمبيعات -----------------
elif current_page == "📈 الصفقات":
    st.subheader("📈 تسجيل صفقة بيع جديدة وتحديد تفاصيل الدفع")
    conn = sqlite3.connect(DB_PATH)
    products_list = pd.read_sql("SELECT id, name, quantity, price FROM products_catalog WHERE quantity > 0", conn)
    emps_list = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
    conn.close()

    if not products_list.empty and emps_list:
        with st.form("make_sale", clear_on_submit=True):
            client_sale_name = st.text_input("اسم العميل:")
            client_phone_sale = st.text_input("رقم هاتف العميل (مهم للآجل والعربون):")
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
                    st.success("🎉 تمت الصفقة وتسجيلها في الحسابات والديون بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ الكمية المطلوبة غير متوفرة بالمخزون.")
                    conn.close()
    else:
        st.warning("⚠️ يرجى إضافة موظفين ومنتجات متوفرة بالمخزون أولاً.")

# ----------------- 5. التقارير -----------------
elif current_page == "📊 التقارير":
    st.subheader("📊 تقارير المبيعات والأداء التفصيلية")
    conn = sqlite3.connect(DB_PATH)
    df_sales_rep = pd.read_sql("SELECT * FROM sales WHERE status != 'ملغاة'", conn)
    conn.close()
    if not df_sales_rep.empty:
        st.dataframe(df_sales_rep, use_container_width=True)
        st.download_button("📥 تحميل تقرير المبيعات (CSV)", df_sales_rep.to_csv(index=False).encode('utf-8-sig'), "sales_report.csv", "text/csv")
    else:
        st.info("لا توجد مبيعات مسجلة للتقارير حالياً.")

# ----------------- 6. دفتر الآجل والديون -----------------
elif current_page == "💰 دفتر الآجل والديون":
    st.subheader("💰 إدارة الديون، الآجل، وعربون العملاء وسداد المديونيات")
    
    with st.expander("➕ تسجيل مديونية جديدة أو عربون عميل"):
        with st.form("manual_debt_form", clear_on_submit=True):
            d_client = st.text_input("اسم العميل:")
            d_phone = st.text_input("رقم الهاتف:")
            d_total = st.number_input("إجمالي المبلغ المطلوب:", value=0.0, min_value=0.0)
            d_paid = st.number_input("المبلغ المدفوع (العربون):", value=0.0, min_value=0.0)
            d_due = st.text_input("تاريخ الاستحقاق (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
            
            if st.form_submit_button("حفظ المديونية في الدفتر"):
                if d_client.strip() and d_total > 0:
                    rem = d_total - d_paid
                    stat = "مخلص" if rem <= 0 else "متبقي"
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO debts (client_name, phone, total_amount, paid_amount, remaining, status, due_date) VALUES (?,?,?,?,?,?,?)",
                                 (d_client, d_phone, d_total, d_paid, rem, stat, d_due))
                    conn.commit()
                    conn.close()
                    st.success("✅ تمت إضافة الديون/العربون للدفتر بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ أدخل اسم العميل وإجمالي المبلغ بشكل صحيح.")

    st.markdown("### 💳 تسجيل سداد أو تسوية مديونية عميل")
    conn = sqlite3.connect(DB_PATH)
    df_debts_active = pd.read_sql("SELECT id, client_name, total_amount, paid_amount, remaining FROM debts WHERE status = 'متبقي'", conn)
    conn.close()

    if not df_debts_active.empty:
        debt_options = {f"عميل: {row['client_name']} | المتبقي عليه: {row['remaining']} د.ك": row['id'] for _, row in df_debts_active.iterrows()}
        selected_debt_key = st.selectbox("اختر العميل لتسجيل سداد دفعة جديدة:", list(debt_options.keys()))
        selected_debt_id = debt_options[selected_debt_key]
        
        current_debt_row = df_debts_active[df_debts_active['id'] == selected_debt_id].iloc[0]
        
        with st.form("pay_debt_form"):
            pay_amount_input = st.number_input("قيمة المبلغ المسدد الآن (د.ك):", value=0.0, min_value=0.0)
            if st.form_submit_button("تحديث حساب العميل وسداد المبلغ"):
                if pay_amount_input > 0:
                    new_paid = current_debt_row['paid_amount'] + pay_amount_input
                    new_remaining = current_debt_row['total_amount'] - new_paid
                    new_status = "مخلص" if new_remaining <= 0 else "متبقي"
                    
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("UPDATE debts SET paid_amount = ?, remaining = ?, status = ? WHERE id = ?",
                                 (new_paid, max(0.0, new_remaining), new_status, selected_debt_id))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ تم خصم المبلغ بنجاح! المتبقي الجديد: {max(0.0, new_remaining)} د.ك")
                    st.rerun()
                else:
                    st.error("⚠️ أدخل قيمة صحيحة للسداد.")

    st.divider()
    st.markdown("### 📋 سجل دفتر الآجل والديون بالكامل:")
    conn = sqlite3.connect(DB_PATH)
    df_debts_all = pd.read_sql("SELECT id AS 'ID', client_name AS 'اسم العميل', phone AS 'الهاتف', total_amount AS 'الإجمالي', paid_amount AS 'المدفوع', remaining AS 'المتبقي', status AS 'الحالة', due_date AS 'تاريخ الاستحقاق' FROM debts", conn)
    conn.close()
    if not df_debts_all.empty:
        st.dataframe(df_debts_all, use_container_width=True)
    else:
        st.info("لا توجد ديون أو عربونات مسجلة حالياً.")

# ----------------- 7. المصروفات -----------------
elif current_page == "💸 المصروفات":
    st.subheader("💸 إدارة المصروفات والنثريات المالية")
    with st.form("expense_form", clear_on_submit=True):
        reason = st.text_input("بيان المصروف:")
        amount = st.number_input("المبلغ:", value=0.0, min_value=0.0)
        category = st.selectbox("تصنيف المصروف:", ["نثريات", "إيجار", "رواتب", "نقل وتوصيل", "أخرى"])
        payment_method = st.selectbox("طريقة الدفع:", ["كاش", "تحويل بنكي"])
        if st.form_submit_button("تسجيل المصروف"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO expenses (reason, amount, date, category, payment_method) VALUES (?,?,?,?,?)",
                         (reason, amount, datetime.now().strftime("%Y-%m-%d"), category, payment_method))
            conn.commit()
            conn.close()
            st.success("✅ تم تسجيل المصروف بنجاح!")
            st.rerun()

    conn = sqlite3.connect(DB_PATH)
    df_exp = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    if not df_exp.empty:
        st.dataframe(df_exp, use_container_width=True)
    else:
        st.info("لا توجد مصروفات مسجلة.")

# ----------------- 8. الفواتير -----------------
elif current_page == "🧾 الفواتير":
    st.subheader("🧾 طباعة وإدارة الفواتير الرسمية للعملاء")
    conn = sqlite3.connect(DB_PATH)
    sales_invoices = pd.read_sql("SELECT id, client_name, product_name, price, quantity_sold, date, employee_name, branch FROM sales WHERE status != 'ملغاة'", conn)
    conn.close()
    if not sales_invoices.empty:
        sel_inv_id = st.selectbox("اختر رقم الفاتورة لطباعتها:", sales_invoices['id'].tolist())
        inv_data = sales_invoices[sales_invoices['id'] == sel_inv_id].iloc[0]
        
        st.markdown(f"""
        <div style="border: 2px solid #333; padding: 25px; border-radius: 10px; background: white; color: black; max-width: 500px; margin: auto;">
            <h2 style="text-align: center;">سوق المروة للأثاث والديكور</h2>
            <hr>
            <p><b>رقم الفاتورة:</b> #{inv_data['id']}</p>
            <p><b>التاريخ:</b> {inv_data['date']}</p>
            <p><b>اسم العميل:</b> {inv_data['client_name']}</p>
            <p><b>الفرع:</b> {inv_data['branch']}</p>
            <p><b>الموظف المسؤول:</b> {inv_data['employee_name']}</p>
            <hr>
            <p><b>المنتج:</b> {inv_data['product_name']}</p>
            <p><b>الكمية:</b> {inv_data['quantity_sold']}</p>
            <h3><b>الإجمالي:</b> {inv_data['price']} د.ك</h3>
            <hr>
            <p style="text-align: center; font-size: 12px;">شكراً لتعاملكم معنا - سوق المروة</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 اضغط (Ctrl+P) لطباعة الفاتورة رسمياً.")
    else:
        st.info("لا توجد فواتير متاحة للطباعة.")

# ----------------- 9. المشاريع -----------------
elif current_page == "🏗️ المشاريع":
    st.subheader("🏗️ إدارة المشاريع والتشطيبات والدهانات")
    with st.form("add_project", clear_on_submit=True):
        p_name = st.text_input("اسم المشروع أو العميل:")
        c_name = st.text_input("اسم صاحب المشروع:")
        total_cost = st.number_input("التكلفة الإجمالية:", value=0.0, min_value=0.0)
        paid_cost = st.number_input("المبلغ المدفوع (العربون):", value=0.0, min_value=0.0)
        team = st.text_input("فريق العمل المسؤول:")
        deadline = st.text_input("موعد التسليم:")
        notes = st.text_area("تفاصيل وملاحظات المشروع:")
        if st.form_submit_button("حفظ المشروع الجديد"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO projects (project_name, client_name, status, total_cost, paid_cost, notes, team, deadline) VALUES (?,?,?,?,?,?,?,?)",
                         (p_name, c_name, "قيد التنفيذ", total_cost, paid_cost, notes, team, deadline))
            conn.commit()
            conn.close()
            st.success("✅ تم حفظ المشروع بنجاح!")
            st.rerun()

    conn = sqlite3.connect(DB_PATH)
    df_projects = pd.read_sql("SELECT * FROM projects", conn)
    conn.close()
    if not df_projects.empty:
        st.dataframe(df_projects, use_container_width=True)
    else:
        st.info("لا توجد مشاريع مسجلة حالياً.")

# ----------------- 10. الموظفين -----------------
elif current_page == "🏅 الموظفين":
    st.subheader("🏅 شؤون العاملين وإدارة الموظفين بالكامل")
    
    emp_tab1, emp_tab2, emp_tab3, emp_tab4, emp_tab5 = st.tabs([
        "👥 بيانات الموظفين", 
        "⏱️ الحضور والغياب", 
        "🎁 الحوافز والمكافآت", 
        "🕒 الورديات", 
        "📝 الملاحظات والأداء"
    ])
    
    with emp_tab1:
        with st.form("add_emp", clear_on_submit=True):
            emp_name = st.text_input("اسم الموظف:")
            emp_phone = st.text_input("رقم الهاتف:")
            emp_address = st.text_input("العنوان:")
            emp_role = st.text_input("الوظيفة أو التخصص (نقاش، مشرف، مبيعات...):")
            emp_salary = st.number_input("الراتب الأساسي:", value=0.0, min_value=0.0)
            emp_hire = st.text_input("تاريخ التعيين (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
            if st.form_submit_button("إضافة الموظف الجديد"):
                if emp_name.strip():
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO employees (name, phone, address, role, salary, hire_date) VALUES (?,?,?,?,?,?)",
                                 (emp_name, emp_phone, emp_address, emp_role, emp_salary, emp_hire))
                    conn.commit()
                    conn.close()
                    st.success("✅ تم تسجيل الموظف بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ يرجى إدخال اسم الموظف.")

        conn = sqlite3.connect(DB_PATH)
        df_employees = pd.read_sql("SELECT id AS 'ID', name AS 'الاسم', phone AS 'الهاتف', role AS 'الوظيفة', salary AS 'الراتب', hire_date AS 'تاريخ التعيين' FROM employees", conn)
        conn.close()
        if not df_employees.empty:
            st.dataframe(df_employees, use_container_width=True)
        else:
            st.info("لا يوجد موظفون مسجلون حالياً.")

    with emp_tab2:
        st.markdown("### ⏱️ تسجيل ومتابعة حضور الغياب اليومي")
        conn = sqlite3.connect(DB_PATH)
        emps_list_att = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
        conn.close()

        if emps_list_att:
            with st.form("attendance_form", clear_on_submit=True):
                att_emp = st.selectbox("اختر الموظف:", emps_list_att)
                att_status = st.selectbox("الحالة:", ["حاضر", "غائب", "إجازة", "مأمورية"])
                att_date = st.text_input("التاريخ:", value=datetime.now().strftime("%Y-%m-%d"))
                if st.form_submit_button("تسجيل الحضور"):
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO employee_attendance (employee_name, date, status) VALUES (?,?,?)", (att_emp, att_date, att_status))
                    conn.commit()
                    conn.close()
                    st.success("✅ تم تسجيل حالة الحضور بنجاح!")
                    st.rerun()

            conn = sqlite3.connect(DB_PATH)
            df_att = pd.read_sql("SELECT employee_name AS 'الموظف', date AS 'التاريخ', status AS 'الحالة' FROM employee_attendance", conn)
            conn.close()
            if not df_att.empty:
                st.dataframe(df_att, use_container_width=True)
        else:
            st.warning("⚠️ يرجى تسجيل موظفين أولاً.")

    with emp_tab3:
        st.markdown("### 🎁 منح الحوافز والمكافآت للعاملين")
        conn = sqlite3.connect(DB_PATH)
        emps_list_bon = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
        conn.close()

        if emps_list_bon:
            with st.form("bonus_form", clear_on_submit=True):
                bon_emp = st.selectbox("اختر الموظف المكافئ:", emps_list_bon)
                bon_amount = st.number_input("قيمة الحافز (د.ك):", value=0.0, min_value=0.0)
                bon_reason = st.text_input("سبب المكافأة / الحافز:")
                bon_date = st.text_input("التاريخ:", value=datetime.now().strftime("%Y-%m-%d"))
                if st.form_submit_button("صرف وحفظ الحافز"):
                    if bon_amount > 0:
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("INSERT INTO employee_bonuses (employee_name, amount, reason, date) VALUES (?,?,?,?)", (bon_emp, bon_amount, bon_reason, bon_date))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم تسجيل الحافز بنجاح!")
                        st.rerun()
                    else:
                        st.error("⚠️ أدخل قيمة الحافز بشكل صحيح.")

            conn = sqlite3.connect(DB_PATH)
            df_bon = pd.read_sql("SELECT employee_name AS 'الموظف', amount AS 'قيمة الحافز', reason AS 'السبب', date AS 'التاريخ' FROM employee_bonuses", conn)
            conn.close()
            if not df_bon.empty:
                st.dataframe(df_bon, use_container_width=True)
        else:
            st.warning("⚠️ يرجى تسجيل موظفين أولاً.")

    with emp_tab4:
        st.markdown("### 🕒 جدولة ورديات العمل للموظفين")
        conn = sqlite3.connect(DB_PATH)
        emps_list_sh = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
        conn.close()

        if emps_list_sh:
            with st.form("shift_form", clear_on_submit=True):
                sh_emp = st.selectbox("الموظف:", emps_list_sh)
                sh_type = st.selectbox("نوع الوردية:", ["الوردية الصباحية (8 ص - 4 م)", "الوردية المسائية (4 م - 12 ص)", "وردية كاملة"])
                sh_date = st.text_input("تاريخ الوردية:", value=datetime.now().strftime("%Y-%m-%d"))
                if st.form_submit_button("تعيين الوردية"):
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO employee_shifts (employee_name, shift_type, date) VALUES (?,?,?)", (sh_emp, sh_type, sh_date))
                    conn.commit()
                    conn.close()
                    st.success("✅ تم تعيين الوردية بنجاح!")
                    st.rerun()

            conn = sqlite3.connect(DB_PATH)
            df_sh = pd.read_sql("SELECT employee_name AS 'الموظف', shift_type AS 'الوردية', date AS 'التاريخ' FROM employee_shifts", conn)
            conn.close()
            if not df_sh.empty:
                st.dataframe(df_sh, use_container_width=True)
        else:
            st.warning("⚠️ يرجى تسجيل موظفين أولاً.")

    with emp_tab5:
        st.markdown("### 📝 تقييم وملاحظات أداء الموظفين")
        conn = sqlite3.connect(DB_PATH)
        emps_list_note = pd.read_sql("SELECT name FROM employees", conn)['name'].tolist()
        conn.close()

        if emps_list_note:
            with st.form("note_form", clear_on_submit=True):
                note_emp = st.selectbox("الموظف المراد تقييمه:", emps_list_note)
                note_text = st.text_area("الملاحظات الإدارية / تقييم الأداء:")
                note_date = st.text_input("التاريخ:", value=datetime.now().strftime("%Y-%m-%d"))
                if st.form_submit_button("حفظ الملاحظة"):
                    if note_text.strip():
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("INSERT INTO employee_notes (employee_name, note, date) VALUES (?,?,?)", (note_emp, note_text, note_date))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم حفظ الملاحظة الإدارية بنجاح!")
                        st.rerun()
                    else:
                        st.error("⚠️ يرجى كتابة محتوى الملاحظة.")

            conn = sqlite3.connect(DB_PATH)
            df_notes = pd.read_sql("SELECT employee_name AS 'الموظف', note AS 'الملاحظة الإدارية', date AS 'التاريخ' FROM employee_notes", conn)
            conn.close()
            if not df_notes.empty:
                st.dataframe(df_notes, use_container_width=True)
        else:
            st.warning("⚠️ يرجى تسجيل موظفين أولاً.")

st.divider()
st.caption("نظام إدارة سوق المروة للأثاث والديكور - النسخة النهائية المطورة 2026")
