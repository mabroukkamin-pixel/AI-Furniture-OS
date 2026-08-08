import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode
import asyncio
import edge_tts

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
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS products_catalog (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, barcode TEXT, image_path TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT, interest TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product_name TEXT, price REAL, quantity_sold INTEGER, date TEXT, employee_name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, amount REAL, category TEXT, date TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, remaining REAL, notes TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT, salary REAL, phone TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT, client_name TEXT, status TEXT, budget REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS product_scripts (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, script_text TEXT, audio_path TEXT)")

    cursor.execute("PRAGMA table_info(clients)")
    c_cols = [col[1] for col in cursor.fetchall()]
    if "name" not in c_cols: cursor.execute("ALTER TABLE clients ADD COLUMN name TEXT")
    if "phone" not in c_cols: cursor.execute("ALTER TABLE clients ADD COLUMN phone TEXT")
    if "address" not in c_cols: cursor.execute("ALTER TABLE clients ADD COLUMN address TEXT")
    if "interest" not in c_cols: cursor.execute("ALTER TABLE clients ADD COLUMN interest TEXT")

    conn.commit()
    conn.close()

init_db()

# --- دالة التنظيف والتصحيح اللغوي الدقيق لمنع أي أخطاء في النطق ---
def normalize_text(text):
    replacements = {
        "×": " في ",
        "x": " في ",
        "/": " شرطة ",
        "سم": " سنتيمتر ",
        "1": "واحد ", "2": "اثنان ", "3": "ثلاثة ", "4": "أربعة ", 
        "5": "خمسة ", "6": "ستة ", "7": "سبعة ", "8": "ثمانية ", "9": "تسعة ", "0": "صفر "
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

st.title("🛒 سوق المروة للأثاث والديكور - (النظام المتكامل للمنتجات الناطقة)")

tabs = st.tabs([
    "📊 المؤشرات", "📦 المخزون والمنتجات الناطقة", "🖨️ QR Code", "👥 العملاء", 
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
    
    tot_sales = df_s['price'].sum() if not df_s.empty and 'price' in df_s.columns else 0
    tot_exp = df_e['amount'].sum() if not df_e.empty and 'amount' in df_e.columns else 0
    tot_debts = df_d['remaining'].sum() if not df_d.empty and 'remaining' in df_d.columns else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 المبيعات", f"{tot_sales:,.1f}")
    c2.metric("💸 المصروفات", f"{tot_exp:,.1f}")
    c3.metric("📈 صافي الربح", f"{tot_sales - tot_exp:,.1f}")
    c4.metric("⚠️ الديون الآجلة", f"{tot_debts:,.1f}")

# 2. المخزون والمنتجات الناطقة والتعديل (الجدول أولاً - والإضافة والتعديل في الأسفل)
with tabs[1]:
    st.subheader("📦 إدارة المخزون وتفعيل خاصية 'المنتج الناطق' بدقة فائقة")
    conn = sqlite3.connect(DB_PATH)
    
    search_q = st.text_input("🔍 بحث سريع في المخزون (بالاسم أو الباركود):")
    if search_q:
        df_p = pd.read_sql(f"SELECT * FROM products_catalog WHERE name LIKE '%{search_q}%' OR barcode LIKE '%{search_q}%'", conn)
    else:
        df_p = pd.read_sql("SELECT * FROM products_catalog ORDER BY id ASC", conn)
        
    st.dataframe(df_p, use_container_width=True)
    
    if not df_p.empty:
        st.markdown("---")
        st.subheader("🎙️ توليد شخصية وخطاب وصوت المنتج الناطق (بدون أخطاء)")
        sel_prod_id = st.selectbox("اختر المنتج لتوليد شخصيته وكلامه التفاعلي:", df_p['id'].tolist(), key="talk_prod")
        selected_row = df_p[df_p['id'] == sel_prod_id].iloc[0]
        
        if st.button("✨ توليد السكريبت والصوت الاحترافي"):
            p_name = str(selected_row.get('name', 'المنتج'))
            p_dims = str(selected_row.get('dims', 'غير محدد'))
            p_color = str(selected_row.get('color', 'طبيعي'))
            p_price = str(selected_row.get('price', 0))
            
            raw_script = f"أهلاً بيك يا غالي.. أنا {p_name}. لوني {p_color}. مقاساتي {p_dims}. سعري {p_price} دينار. قطعة متفصلة لإنسان بيفهم في الجودة.. ها.. تاخدني أنور بيتك؟"
            
            clean_script = normalize_text(raw_script)
            
            os.makedirs("audio_outputs", exist_ok=True)
            audio_filename = f"audio_outputs/product_{sel_prod_id}.mp3"
            
            voice = "ar-EG-ShakirNeural"
            communicate = edge_tts.Communicate(clean_script, voice, rate="-5%", pitch="-5Hz")
            
            asyncio.run(communicate.save(audio_filename))
            
            st.info(raw_script)
            st.audio(audio_filename, format='audio/mp3')
            
            conn.execute("INSERT OR REPLACE INTO product_scripts (product_id, script_text, audio_path) VALUES (?, ?, ?)", 
                         (sel_prod_id, raw_script, audio_filename))
            conn.commit()
            st.success("تم توليد السكريبت والصوت النقي بنجاح!")

    st.markdown("---")
    st.markdown("### ⚙️ عمليات الإضافة، التعديل، والحذف (أسفل الصفحة)")

    with st.expander("➕ إضافة منتج جديد بالتفاصيل والصورة"):
        with st.form("add_prod_orig", clear_on_submit=True):
            cat = st.text_input("التصنيف (مثال: غرف نوم، طاولات):")
            name = st.text_input("اسم المنتج:")
            color = st.text_input("اللون:")
            dims = st.text_input("المقاسات (مثال: 40×53×120 سم):")
            price = st.number_input("السعر:", min_value=0.0)
            quantity = st.number_input("الكمية:", min_value=0, step=1)
            location = st.text_input("الموقع (المعرض أو المخزن):")
            barcode = st.text_input("كود الباركود / QR (مثل: AMIN1995):")
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

    if not df_p.empty:
        with st.expander("✏️ تعديل بيانات منتج موجود"):
            edit_p_id = st.selectbox("اختر رقم معرف المنتج (ID) للتعديل:", df_p['id'].tolist(), key="edit_prod_sel")
            p_row = df_p[df_p['id'] == edit_p_id].iloc[0]
            
            with st.form("edit_prod_form"):
                e_cat = st.text_input("التصنيف:", value=str(p_row.get('category', '')))
                e_name = st.text_input("اسم المنتج:", value=str(p_row.get('name', '')))
                e_color = st.text_input("اللون:", value=str(p_row.get('color', '')))
                e_dims = st.text_input("المقاسات:", value=str(p_row.get('dims', '')))
                e_price = st.number_input("السعر:", min_value=0.0, value=float(p_row.get('price', 0.0)))
                e_qty = st.number_input("الكمية:", min_value=0, step=1, value=int(p_row.get('quantity', 0)))
                e_loc = st.text_input("الموقع:", value=str(p_row.get('location', '')))
                e_bar = st.text_input("الباركود:", value=str(p_row.get('barcode', '')))
                
                if st.form_submit_button("تحديث المنتج"):
                    conn.execute("""
                        UPDATE products_catalog 
                        SET category=?, name=?, color=?, dims=?, price=?, quantity=?, location=?, barcode=? 
                        WHERE id=?
                    """, (e_cat, e_name, e_color, e_dims, e_price, e_qty, e_loc, e_bar, edit_p_id))
                    conn.commit()
                    st.success("تم تحديث المنتج بنجاح!")
                    st.rerun()

        with st.expander("🗑️ حذف منتج من المخزون"):
            del_p_id = st.selectbox("اختر رقم معرف المنتج (ID) للحذف:", df_p['id'].tolist(), key="del_prod_sel")
            if st.button("تأكيد حذف المنتج"):
                conn.execute("DELETE FROM products_catalog WHERE id = ?", (del_p_id,))
                conn.commit()
                st.success("تم حذف المنتج بنجاح!")
                st.rerun()
                
    conn.close()

# 3. توليد QR Code
with tabs[2]:
    st.subheader("🖨️ توليد وطباعة QR Code للاستيكر الناطق")
    q_text = st.text_input("أدخل كود الباركود للربط مع المنتج الناطق:", value="AMIN1995")
    if st.button("إنشاء الاستيكر"):
        if q_text.strip() != "":
            img = qrcode.make(q_text)
            img.save("qrcode_gen.png")
            st.image("qrcode_gen.png", width=250)
            st.success("تم توليد الـ QR Code الناطق بنجاح وجاهز للطباعة واللزق على القطعة.")
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
    if not df_sales.empty and 'product_name' in df_sales.columns and 'quantity_sold' in df_sales.columns:
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
    st.subheader("🏅 شؤون الموظفين وفريق العمل")
    conn = sqlite3.connect(DB_PATH)
    df_em = pd.read_sql("SELECT * FROM employees ORDER BY id ASC", conn)
    
    if not df_em.empty and 'salary' in df_em.columns:
        tot_salaries = df_em['salary'].sum()
        c1, c2 = st.columns(2)
        c1.metric("👥 إجمالي عدد الموظفين", len(df_em))
        c2.metric("💸 إجمالي الرواتب الشهرية", f"{tot_salaries:,.1f}")
        st.markdown("---")
    
    st.dataframe(df_em, use_container_width=True)
    
    with st.expander("➕ إضافة موظف أو فني جديد"):
        with st.form("add_emp_full", clear_on_submit=True):
            em_name = st.text_input("اسم الموظف أو الصنايعي:")
            em_role = st.text_input("التخصص (فني دهان، نقاش، مشرف، إلخ):")
            em_sal = st.number_input("الراتب المتفق عليه:", min_value=0.0)
            em_phone = st.text_input("رقم الهاتف / التواصل:")
            
            if st.form_submit_button("حفظ بيانات الموظف"):
                conn.execute("INSERT INTO employees (name, role, salary, phone) VALUES (?,?,?,?)", 
                             (em_name, em_role, em_sal, em_phone))
                conn.commit()
                st.success("تم إضافة الموظف بنجاح!")
                st.rerun()

    if not df_em.empty:
        with st.expander("✏️ تعديل بيانات موظف"):
            edit_emp_id = st.selectbox("اختر رقم معرف الموظف (ID) للتعديل:", df_em['id'].tolist(), key="edit_emp_sel")
            emp_row = df_em[df_em['id'] == edit_emp_id].iloc[0]
            
            with st.form("edit_emp_form"):
                e_name = st.text_input("اسم الموظف:", value=str(emp_row['name']) if 'name' in emp_row and pd.notna(emp_row['name']) else '')
                e_role = st.text_input("التخصص / الوظيفة:", value=str(emp_row['role']) if 'role' in emp_row and pd.notna(emp_row['role']) else '')
                e_sal = st.number_input("الراتب:", min_value=0.0, value=float(emp_row['salary']) if 'salary' in emp_row and pd.notna(emp_row['salary']) else 0.0)
                e_phone = st.text_input("رقم الهاتف:", value=str(emp_row['phone']) if 'phone' in emp_row and pd.notna(emp_row['phone']) else '')
                
                if st.form_submit_button("تحديث بيانات الموظف"):
                    conn.execute("""
                        UPDATE employees 
                        SET name=?, role=?, salary=?, phone=? 
                        WHERE id=?
                    """, (e_name, e_role, e_sal, e_phone, edit_emp_id))
                    conn.commit()
                    st.success("تم تحديث بيانات الموظف بنجاح!")
                    st.rerun()

        with st.expander("🗑️ حذف موظف من القائمة"):
            del_emp_id = st.selectbox("اختر رقم معرف الموظف (ID) للحذف:", df_em['id'].tolist(), key="del_emp_sel")
            if st.button("تأكيد حذف الموظف"):
                conn.execute("DELETE FROM employees WHERE id = ?", (del_emp_id,))
                conn.commit()
                st.success("تم حذف الموظف بنجاح!")
                st.rerun()
                
    conn.close()
