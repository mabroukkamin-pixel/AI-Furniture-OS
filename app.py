import streamlit as st
import pandas as pd
import requests

SHEET_ID = '1hyWigWYiVsRPQH3tYz2Oxyilo9yDs4p_Q0R0AHk_SGU'
WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbxQJ4VEzVOaChGCrRP9fdFlQjcCH41By2VrTWPt_jdgh9Tq26UGBQO7RVXDmL8PAVJA/exec'

st.title("👑 النظام العالمي لإدارة العمليات")

@st.cache_data
def load_data():
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Products'
    return pd.read_csv(url)

df = load_data()

product_name = st.selectbox("اختر المنتج:", df['Product_Name'].unique())
product_details = df[df['Product_Name'] == product_name].iloc[0]

st.write(f"### تفاصيل المنتج: {product_name}")
st.write(f"- **السعر:** {product_details['Price']} دينار")
st.write(f"- **المقاسات:** {product_details['Dimensions']}")
st.write(f"- **اللون:** {product_details['Color']}")

st.write("---")
st.subheader("إصدار فاتورة جديدة")

with st.form("order_form", clear_on_submit=True):
    client_name = st.text_input("اسم العميل")
    phone = st.text_input("رقم الهاتف")
    
    if st.form_submit_button("حفظ الطلب في النظام"):
        if client_name and phone:
            order_data = {
                "client_name": client_name,
                "phone": phone,
                "product_name": product_name,
                "price": str(product_details['Price'])
            }
            try:
                response = requests.post(WEB_APP_URL, json=order_data)
                if response.status_code == 200:
                    st.success(f"تم تسجيل طلب العميل {client_name} بنجاح وترحيله إلى قاعدة البيانات!")
                else:
                    st.error("حدث خطأ أثناء الاتصال بقاعدة البيانات.")
            except Exception as e:
                st.error(f"خطأ في الإرسال: {e}")
        else:
            st.error("يرجى ملء جميع البيانات.")
