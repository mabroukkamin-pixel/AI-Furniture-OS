import streamlit as st
import pandas as pd

# رابط ملفك السحابي
SHEET_ID = '1hyWigWYiVsRPQH3tYz2Oxyilo9yDs4p_Q0R0AHk_SGU'
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Products'

st.set_page_config(page_title="النظام العالمي لإدارة العمليات", layout="wide")
st.title("👑 النظام العالمي لإدارة العمليات")

@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    products_db = dict(zip(df['Product_Name'], df['Price']))
except:
    products_db = {"خطأ في تحميل البيانات": 0}

menu = st.sidebar.selectbox("اختر القسم:", ["إدارة التصميم", "إدارة الحسابات", "دليل حل المشكلات"])

if menu == "إدارة الحسابات":
    st.header("إدارة الحسابات (قراءة مباشرة من السحابة)")
    selected_product = st.selectbox("اختر المنتج:", list(products_db.keys()))
    st.write(f"السعر المعتمد: **{products_db[selected_product]} دينار**")

    with st.form("order_form"):
        client_name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        if st.form_submit_button("إصدار الفاتورة"):
            st.success(f"تم تسجيل طلب {client_name} بنجاح!")
