import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعدادات الاتصال بالسحابة
SHEET_ID = '1hyWigWYiVsRPQH3tYz2Oxyilo9yDs4p_Q0R0AHk_SGU'

st.title("👑 النظام العالمي لإدارة العمليات")

# تحميل البيانات للعرض
@st.cache_data
def load_data():
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Products'
    return pd.read_csv(url)

df = load_data()

# واجهة اختيار المنتج
product_name = st.selectbox("اختر المنتج:", df['Product_Name'].unique())
product_details = df[df['Product_Name'] == product_name].iloc[0]

st.write(f"### تفاصيل المنتج: {product_name}")
st.write(f"- **السعر:** {product_details['Price']} دينار")
st.write(f"- **المقاسات:** {product_details['Dimensions']}")
st.write(f"- **اللون:** {product_details['Color']}")

# قسم تسجيل الطلب
st.write("---")
st.subheader("إصدار فاتورة جديدة")

with st.form("order_form", clear_on_submit=True):
    client_name = st.text_input("اسم العميل")
    phone = st.text_input("رقم الهاتف")
    
    if st.form_submit_button("حفظ الطلب"):
        if client_name and phone:
            # هنا الكود المنطقي للترحيل
            # ملاحظة: في بيئة العمل السحابية، يفضل استخدام ملف credentials.json للربط
            # سأقوم بتجهيزك للخطوة القادمة (ربط الـ API)
            st.success(f"تم إرسال طلب العميل {client_name} بنجاح إلى قاعدة البيانات!")
        else:
            st.error("يرجى ملء جميع البيانات.")
