import streamlit as st
import sqlite3
import datetime
import pandas as pd

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sovereign_logs (
        id INTEGER PRIMARY KEY, 
        user_role TEXT, 
        action_name TEXT, 
        details TEXT, 
        financial_val REAL, 
        currency TEXT, 
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="👑 الإمبراطورية السيادية - العابرة للحدود", layout="wide")

st.sidebar.title("🔐 بوابة الدخول السيادية")
user_role = st.sidebar.selectbox("حدد صفوتك / دورك في النظام:", [
    "👑 القائد الأعلى (أمين مبروك - مصر)",
    "🤝 النائب السيادي (أخوك - الكويت)",
    "💰 مسؤول الحسابات (الكويت)",
    "🛒 مسؤول السوق والمبيعات (الكويت)",
    "🎨 مسؤول التصميم والتنفيذ (الكويت)"
])

st.sidebar.divider()
st.sidebar.info("🌐 النظام متصل مركزياً ومجاني 100% عبر السحابة.")

if "القائد الأعلى" in user_role or "النائب السيادي" in user_role:
    st.title(f"👑 لوحة القيادة المركزية - {user_role}")
    st.success("أنت تمتلك الصلاحيات المطلقة للتحكم ومراجعة العمليات من أي مكان وفي أي وقت.")
    
    tab1, tab2, tab3 = st.tabs(["📊 نظرة عامة شاملة", "⚙️ إدارة العمليات", "🛡️ سجل الإمبراطورية"])
    
    with tab1:
        st.metric(label="حالة العمليات السيادية", value="متصل بالسحابة بنجاح")
        st.write("متابعة حية لكل ما يفعله فريق الكويت لحظة بلحظة.")
        
    with tab2:
        action_type = st.selectbox("اختر نوع العملية:", ["تعديل سعر/منتج", "إقرار عقد جديد", "مراجعة سيولة مالية", "أمر طوارئ"])
        details = st.text_area("تفاصيل القرار أو التوجيه:")
        val = st.number_input("القيمة (إن وجدت):", value=0.0)
        curr = st.selectbox("العملة:", ["جنيه مصري (EGP)", "دينار كويتي (KWD)"])
        if st.button("تنفيذ وتعميم القرار فوراً"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO sovereign_logs (user_role, action_name, details, financial_val, currency, timestamp) VALUES (?,?,?,?,?,?)",
                      (user_role, action_type, details, val, curr, str(datetime.datetime.now())))
            conn.commit()
            conn.close()
            st.success("✅ تم تنفيذ القرار وتحديث السحابة بنجاح!")
            st.rerun()
            
    with tab3:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM sovereign_logs ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

elif "مسؤول الحسابات" in user_role:
    st.title("💰 شاشة الحسابات والماليات (الكويت)")
    st.write("مخصص فقط لتسجيل الفواتير، القبض، والمصروفات.")
    client = st.text_input("اسم العميل / الجهة:")
    amount = st.number_input("المبلغ التحصيلي:", value=0.0)
    curr = st.selectbox("العملة:", ["دينار كويتي (KWD)", "جنيه مصري (EGP)"])
    if st.button("حفظ القيد المالي"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sovereign_logs (user_role, action_name, details, financial_val, currency, timestamp) VALUES (?,?,?,?,?,?)",
                  (user_role, "قيد مالي", f"تحصيل من: {client}", amount, curr, str(datetime.datetime.now())))
        conn.commit()
        conn.close()
        st.success("✅ تم تسجيل المعاملة المالية ووصولها للرئيس في مصر فوراً!")

elif "مسؤول السوق والمبيعات" in user_role:
    st.title("🛒 شاشة إدارة السوق والمبيعات (الكويت)")
    st.write("مخصص لمتابعة العملاء وحالة المعرض والطلبيات.")
    cust_name = st.text_input("اسم العميل الجديد:")
    req_details = st.text_area("تفاصيل الطلبية أو البضاعة:")
    if st.button("إثبات طلبية السوق"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sovereign_logs (user_role, action_name, details, financial_val, currency, timestamp) VALUES (?,?,?,?,?,?)",
                  (user_role, "طلبية سوق", f"عميل: {cust_name} - طلب: {req_details}", 0.0, "دينار كويتي (KWD)", str(datetime.datetime.now())))
        conn.commit()
        conn.close()
        st.success("✅ تم تسجيل الطلبية في النظام المركزي بنجاح!")

else:
    st.title("🎨 شاشة التصميم والتنفيذ (الكويت)")
    st.write("مخصص لتلقي مقاسات وتصاميم الأثاث والتشطيبات.")
    design_note = st.text_area("تفاصيل التصميم المنفذ أو المقاسات:")
    if st.button("تحديث حالة التصميم"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sovereign_logs (user_role, action_name, details, financial_val, currency, timestamp) VALUES (?,?,?,?,?,?)",
                  (user_role, "تصميم وتنفيذ", design_note, 0.0, "دينار كويتي (KWD)", str(datetime.datetime.now())))
        conn.commit()
        conn.close()
        st.success("✅ تم إرسال حالة التصميم للقيادة بنجاح!")
